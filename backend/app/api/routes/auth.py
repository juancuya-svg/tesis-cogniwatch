from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserRegister

router = APIRouter()


@router.post('/register', response_model=TokenResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already exists')
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.email)
    return TokenResponse(access_token=token, role=user.role)


@router.post('/login', response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail='Invalid email or password')
    token = create_access_token(user.email)
    return TokenResponse(access_token=token, role=user.role)


@router.get('/me')
def me(user: User = Depends(get_current_user)) -> dict:
    return {
        'id': user.id,
        'full_name': user.full_name,
        'email': user.email,
        'role': user.role,
    }
