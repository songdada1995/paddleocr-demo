from sqlalchemy.orm import Session
from app.models.client import Client, Token
from app.schemas.client import ClientCreate, TokenCreate
from app.core.security import get_password_hash
from datetime import datetime, timezone

def get_client_by_client_id(db: Session, client_id: str):
    return db.query(Client).filter(Client.client_id == client_id).first()

def create_client(db: Session, client: ClientCreate):
    hashed_secret = get_password_hash(client.client_secret)
    db_client = Client(
        client_id=client.client_id,
        hashed_secret=hashed_secret,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        token_version=0
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Token相关CRUD

def create_token(db: Session, token: TokenCreate):
    db_token = Token(
        client_id=token.client_id,
        token=token.token,
        issued_at=token.issued_at,
        expires_at=token.expires_at,
        ip=token.ip,
        user_agent=token.user_agent,
        is_active=True
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def revoke_token(db: Session, token_str: str):
    db_token = db.query(Token).filter(Token.token == token_str, Token.is_active == True).first()
    if db_token:
        setattr(db_token, 'is_active', False)
        setattr(db_token, 'revoked_at', datetime.utcnow())
        db.commit()
        db.refresh(db_token)
    return db_token

def get_active_token(db: Session, token_str: str):
    return db.query(Token).filter(Token.token == token_str, Token.is_active == True).first()

def get_tokens_by_client(db: Session, client_id: str):
    return db.query(Token).filter(Token.client_id == client_id).all()