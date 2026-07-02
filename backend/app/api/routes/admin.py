from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.patient import Alert, PatientProfile, WearableDailySummary
from app.models.user import User

router = APIRouter()


@router.get('/summary')
def admin_summary(db: Session = Depends(get_db), _: User = Depends(require_role('admin'))):
    return {
        'patients': db.query(User).filter(User.role == 'patient').count(),
        'caregivers': db.query(User).filter(User.role == 'caregiver').count(),
        'alerts_total': db.query(Alert).count(),
        'signals_total': db.query(WearableDailySummary).count(),
    }
