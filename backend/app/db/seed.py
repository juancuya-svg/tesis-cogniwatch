from datetime import date, timedelta
import random

from app.core.db import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models.patient import Alert, BaselineAssessment, CaregiverLink, CognitiveMotorSession, PatientProfile, WearableDailySummary
from app.models.user import User


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print('Seed skipped: users already exist')
            return

        admin = User(full_name='CogniWatch Admin', email='admin@cogniwatch.local', password_hash=get_password_hash('ChangeMe123!'), role='admin')
        caregiver = User(full_name='Laura Flores', email='caregiver@cogniwatch.local', password_hash=get_password_hash('ChangeMe123!'), role='caregiver')
        patient = User(full_name='Carlos Vega', email='patient@cogniwatch.local', password_hash=get_password_hash('ChangeMe123!'), role='patient')
        db.add_all([admin, caregiver, patient])
        db.flush()

        profile = PatientProfile(
            user_id=patient.id,
            sex_at_birth='male',
            monitoring_reason='memory_follow_up',
            autonomy_level='partial_support',
            baseline_tier='watchlist',
            consent_signed=True,
            wearable_connected=True,
        )
        db.add(profile)
        db.add(CaregiverLink(caregiver_user_id=caregiver.id, patient_user_id=patient.id, relationship_label='daughter'))
        db.add(BaselineAssessment(
            patient_user_id=patient.id,
            perceived_memory=2,
            perceived_attention=1,
            sleep_hours=6.5,
            activity_days=4,
            autonomy_score=2,
            self_report_score=0.42,
            suggested_tier='watchlist',
            assessment_payload={'source': 'demo_seed'},
        ))

        start = date.today() - timedelta(days=14)
        for i in range(14):
            dt = start + timedelta(days=i)
            db.add(WearableDailySummary(
                patient_user_id=patient.id,
                summary_date=dt,
                total_sleep_minutes=420 + random.randint(-50, 35),
                sleep_efficiency=0.82 + random.uniform(-0.06, 0.04),
                awakenings=2 + random.randint(0, 3),
                steps=5200 + random.randint(-1800, 2200),
                sedentary_minutes=540 + random.randint(-50, 60),
                active_minutes=60 + random.randint(-20, 25),
                avg_heart_rate=76 + random.uniform(-4, 5),
                resting_heart_rate=67 + random.uniform(-4, 4),
                hrv=32 + random.uniform(-8, 8),
                spo2=97 + random.uniform(-1, 1),
                respiratory_rate=15 + random.uniform(-1.5, 1.2),
                wear_adherence=0.85 + random.uniform(-0.2, 0.1),
            ))

        db.add(CognitiveMotorSession(
            patient_user_id=patient.id,
            session_type='finger_trace',
            total_time_ms=24300,
            mean_speed=3.18,
            mean_jerk=0.086,
            air_time_ratio=0.21,
            pressure_mean=0.0,
            predicted_flag_probability=0.41,
            feature_payload={'task': 'spiral_trace', 'source': 'demo_seed'},
        ))

        db.add(Alert(
            patient_user_id=patient.id,
            alert_type='activity_drop',
            severity='medium',
            status='new',
            title='Actividad reducida frente a línea base',
            explanation='Los pasos diarios bajaron frente al patrón personal de las últimas dos semanas.',
            recommendation='Confirmar si hubo fatiga, mal descanso o menor uso del reloj.',
            score=0.34,
            alert_payload={'source': 'demo_seed'},
        ))
        db.commit()
        print('Demo seed created successfully')
    finally:
        db.close()


if __name__ == '__main__':
    run()
