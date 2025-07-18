from fastapi import APIRouter, Depends, HTTPException, Request, status, Security, Form, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime
import base64

from app import crud
from app.core import security as core_security
from app.core.config import settings
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.client import TokenCreate, ClientCreate, Client as ClientSchema

router = APIRouter()
security = HTTPBearer()

def parse_basic_auth(authorization: str):
    if not authorization or not authorization.startswith("Basic "):
        return None, None
    b64 = authorization[6:]
    try:
        decoded = base64.b64decode(b64).decode()
        client_id, client_secret = decoded.split(":", 1)
        return client_id, client_secret
    except Exception:
        return None, None

@router.post("/token")
def login_for_access_token(
    request: Request,
    grant_type: str = Form(default="client_credentials"),
    client_id: str = Form(default=None),
    client_secret: str = Form(default=None),
    authorization: str = Header(default=None),
    db: Session = Depends(get_db)
):
    if grant_type != "client_credentials":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    # 优先解析Basic Auth
    basic_id, basic_secret = parse_basic_auth(authorization)
    if basic_id and basic_secret:
        client_id = basic_id
        client_secret = basic_secret
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="Missing client_id or client_secret")
    client = crud.client.get_client_by_client_id(db, client_id=client_id)
    if not client or not core_security.verify_password(client_secret, str(client.hashed_secret)):
        raise HTTPException(
            status_code=400,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not bool(client.is_active):
        raise HTTPException(status_code=400, detail="Inactive client")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.now()
    expire = now + access_token_expires
    access_token = core_security.create_access_token(
        data={"sub": str(client.client_id)}, expires_delta=access_token_expires
    )
    crud.client.create_token(db, TokenCreate(
        client_id=str(client.client_id),
        token=access_token,
        issued_at=now,
        expires_at=expire,
        ip=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None
    ))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "scope": "default"
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_token = crud.client.revoke_token(db, token)
    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found or already revoked")
    return None

@router.post("/register", response_model=ClientSchema)
def register_client(
    db: Session = Depends(get_db),
    client_in: ClientCreate = Depends()
):
    db_client = crud.client.get_client_by_client_id(db, client_id=client_in.client_id)
    if db_client:
        raise HTTPException(status_code=400, detail="Client already exists")
    new_client = crud.client.create_client(db, client_in)
    return new_client