from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.models.patient import Alert, BaselineAssessment, CareNote, CaregiverLink, CognitiveMotorSession, PatientProfile, WearableDailySummary
from app.models.user import User
from app.schemas.patient import AlertOut, BaselineAssessmentIn, CognitiveMotorSessionIn, PatientCreate, WearableDailySummaryIn
from app.services.alert_engine import BaselineSnapshot, build_alerts
from app.services.anomaly import anomaly_score
from app.services.scoring import combine_scores
from app.ml.inference import ml_service
from app.core.security import get_password_hash

router = APIRouter()


@router.post('')
def create_patient(payload: PatientCreate, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver'))):
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role='patient',
    )
    db.add(user)
    db.flush()
    profile = PatientProfile(
        user_id=user.id,
        date_of_birth=payload.date_of_birth,
        sex_at_birth=payload.sex_at_birth,
        monitoring_reason=payload.monitoring_reason,
        autonomy_level=payload.autonomy_level,
    )
    db.add(profile)
    db.commit()
    return {'message': 'patient created', 'patient_user_id': user.id}


@router.get('')
def list_patients(db: Session = Depends(get_db), user: User = Depends(require_role('admin', 'caregiver', 'clinician', 'patient'))):
    if user.role == 'patient':
        patient_ids = [user.id]
    elif user.role == 'caregiver':
        patient_ids = [row.patient_user_id for row in db.query(CaregiverLink).filter(CaregiverLink.caregiver_user_id == user.id).all()]
    else:
        patient_ids = [row[0] for row in db.query(User.id).filter(User.role == 'patient').all()]

    patients = db.query(User, PatientProfile).join(PatientProfile, PatientProfile.user_id == User.id).filter(User.id.in_(patient_ids)).all()
    return [
        {
            'id': u.id,
            'full_name': u.full_name,
            'email': u.email,
            'baseline_tier': p.baseline_tier,
            'monitoring_reason': p.monitoring_reason,
            'autonomy_level': p.autonomy_level,
        }
        for u, p in patients
    ]


@router.post('/{patient_user_id}/baseline')
def save_baseline(patient_user_id: int, payload: BaselineAssessmentIn, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'patient'))):
    obj = BaselineAssessment(patient_user_id=patient_user_id, **payload.model_dump())
    db.add(obj)
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == patient_user_id).first()
    if profile:
        features = {
            'age_at_visit': None,
            'SEX': 1 if profile.sex_at_birth == 'male' else 2 if profile.sex_at_birth == 'female' else None,
            'EDUC': None,
            'INDEPEND': payload.autonomy_score,
            'MEMORY': payload.perceived_memory,
            'MEMPROB': payload.assessment_payload.get('memory_problem_flag'),
            'CDRSUM': payload.assessment_payload.get('cdrsum_proxy'),
            'CDRGLOB': payload.assessment_payload.get('cdrglob_proxy'),
            'NACCGDS': payload.assessment_payload.get('gds_proxy'),
            'NACCMMSE': payload.assessment_payload.get('mmse_proxy'),
            'NACCMOCA': payload.assessment_payload.get('moca_proxy'),
            'TRAILA': payload.assessment_payload.get('trail_a_proxy'),
            'TRAILB': payload.assessment_payload.get('trail_b_proxy'),
            'ANXIETY': payload.assessment_payload.get('anxiety_flag'),
            'AGIT': payload.assessment_payload.get('agitation_flag'),
            'HALL': payload.assessment_payload.get('hallucination_flag'),
            'DEL': payload.assessment_payload.get('delusion_flag'),
            'GAIT': payload.assessment_payload.get('gait_issue_flag'),
            'SLEEPAP': payload.assessment_payload.get('sleep_apnea_flag'),
            'BPSYS': payload.assessment_payload.get('bp_sys'),
            'BPDIAS': payload.assessment_payload.get('bp_dias'),
            'PARKSIGN': payload.assessment_payload.get('parkinsonism_flag'),
            'NACCAPOE': None,
        }
        tier, _ = ml_service.predict_monitoring_tier(features)
        profile.baseline_tier = {0: 'low_monitoring', 1: 'watchlist', 2: 'high_support'}.get(tier, 'watchlist')
    db.commit()
    return {'message': 'baseline saved', 'suggested_tier': profile.baseline_tier if profile else 'watchlist'}


@router.post('/{patient_user_id}/signals/daily')
def ingest_daily_summary(patient_user_id: int, payload: WearableDailySummaryIn, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'patient'))):
    obj = WearableDailySummary(patient_user_id=patient_user_id, **payload.model_dump())
    db.add(obj)
    db.flush()

    history = (
        db.query(
            func.avg(WearableDailySummary.total_sleep_minutes),
            func.avg(WearableDailySummary.steps),
            func.avg(WearableDailySummary.resting_heart_rate),
            func.avg(WearableDailySummary.awakenings),
        )
        .filter(WearableDailySummary.patient_user_id == patient_user_id)
        .filter(WearableDailySummary.summary_date < payload.summary_date)
        .all()[0]
    )
    baseline = {
        'total_sleep_minutes': history[0],
        'steps': history[1],
        'resting_heart_rate': history[2],
        'awakenings': history[3],
    }

    anomaly = anomaly_score(payload.model_dump(), baseline)
    raw_alerts = build_alerts(payload.model_dump(), BaselineSnapshot(history[0], history[1], history[2]))
    latest_cognitive = db.query(CognitiveMotorSession).filter(CognitiveMotorSession.patient_user_id == patient_user_id).order_by(CognitiveMotorSession.created_at.desc()).first()

    profile = db.query(PatientProfile).filter(PatientProfile.user_id == patient_user_id).first()
    monitoring_tier = {'low_monitoring': 0, 'watchlist': 1, 'high_support': 2}.get(profile.baseline_tier if profile else 'watchlist', 1)
    composite = combine_scores(monitoring_tier, anomaly, latest_cognitive.predicted_flag_probability if latest_cognitive else None)

    created = []
    for item in raw_alerts:
        alert = Alert(patient_user_id=patient_user_id, status='new', alert_payload=composite, **item)
        db.add(alert)
        created.append(alert.alert_type)
    db.commit()
    return {'message': 'signal saved', 'anomaly_score': anomaly, 'composite': composite, 'alerts_created': created}


@router.post('/{patient_user_id}/cognitive-motor')
def ingest_cognitive_motor(patient_user_id: int, payload: CognitiveMotorSessionIn, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'patient'))):
    probability = None
    feature_payload = payload.feature_payload.copy()
    if feature_payload:
        probability = ml_service.predict_cognitive_motor_probability(feature_payload)
    obj = CognitiveMotorSession(
        patient_user_id=patient_user_id,
        predicted_flag_probability=probability,
        **payload.model_dump(),
    )
    db.add(obj)
    db.commit()
    return {'message': 'cognitive-motor session stored', 'probability': probability}


@router.get('/{patient_user_id}/alerts', response_model=list[AlertOut])
def patient_alerts(patient_user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'clinician', 'patient'))):
    return db.query(Alert).filter(Alert.patient_user_id == patient_user_id).order_by(Alert.created_at.desc()).all()


@router.get('/{patient_user_id}/overview')
def patient_overview(patient_user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'clinician', 'patient'))):
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == patient_user_id).first()
    user = db.query(User).filter(User.id == patient_user_id).first()
    latest_signal = db.query(WearableDailySummary).filter(WearableDailySummary.patient_user_id == patient_user_id).order_by(WearableDailySummary.summary_date.desc()).first()
    latest_cm = db.query(CognitiveMotorSession).filter(CognitiveMotorSession.patient_user_id == patient_user_id).order_by(CognitiveMotorSession.created_at.desc()).first()
    alerts_open = db.query(Alert).filter(Alert.patient_user_id == patient_user_id, Alert.status.in_(['new', 'viewed', 'attended'])).count()
    return {
        'patient': {
            'id': user.id if user else patient_user_id,
            'full_name': user.full_name if user else 'Unknown',
            'baseline_tier': profile.baseline_tier if profile else 'watchlist',
            'monitoring_reason': profile.monitoring_reason if profile else None,
            'wearable_connected': profile.wearable_connected if profile else False,
        },
        'latest_signal': None if latest_signal is None else {
            'summary_date': str(latest_signal.summary_date),
            'sleep': latest_signal.total_sleep_minutes,
            'steps': latest_signal.steps,
            'resting_hr': latest_signal.resting_heart_rate,
            'adherence': latest_signal.wear_adherence,
        },
        'latest_cognitive_motor_probability': latest_cm.predicted_flag_probability if latest_cm else None,
        'open_alerts': alerts_open,
    }
