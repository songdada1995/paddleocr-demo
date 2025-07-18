from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.schemas.token import Token

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    client = crud.client.get_client_by_client_id(db, client_id=form_data.username)
    if not client or not security.verify_password(form_data.password, client.hashed_client_secret):
        raise HTTPException(
            status_code=400,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not client.is_active:
        raise HTTPException(status_code=400, detail="Inactive client")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": client.client_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}