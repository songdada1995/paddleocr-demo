from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db.session import get_db
from app.models.client import Client
from app.crud import client as crud_client
from app.models.client import Token
from datetime import datetime

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)

def get_current_client(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Client:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # 校验token在数据库中有效
    db_token = crud_client.get_active_token(db, token)
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked or not found")
    # 统一用naive时间比较
    expires_at = getattr(db_token, 'expires_at', None)
    if isinstance(expires_at, datetime) and expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    client = crud_client.get_client_by_client_id(db, client_id=token_data.sub or "")
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    is_active = getattr(client, 'is_active', False)
    if is_active is not True:
        raise HTTPException(status_code=400, detail="Inactive client")
    return client