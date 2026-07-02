from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.patient import Alert
from app.models.user import User

router = APIRouter()


@router.get('')
def list_alerts(db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'clinician'))):
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()
    return [
        {
            'id': a.id,
            'patient_user_id': a.patient_user_id,
            'alert_type': a.alert_type,
            'severity': a.severity,
            'status': a.status,
            'title': a.title,
            'explanation': a.explanation,
            'recommendation': a.recommendation,
            'score': a.score,
            'created_at': a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]


@router.patch('/{alert_id}/status')
def update_alert_status(alert_id: int, status: str, db: Session = Depends(get_db), _: User = Depends(require_role('admin', 'caregiver', 'clinician'))):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail='Alert not found')
    alert.status = status
    db.commit()
    return {'message': 'alert updated', 'status': alert.status}
