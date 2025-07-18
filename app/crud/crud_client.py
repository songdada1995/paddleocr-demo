from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate
from app.core.security import get_password_hash

def get_client_by_client_id(db: Session, client_id: str):
    return db.query(Client).filter(Client.client_id == client_id).first()

def create_client(db: Session, client: ClientCreate):
    hashed_secret = get_password_hash(client.client_secret)
    db_client = Client(client_id=client.client_id, hashed_client_secret=hashed_secret)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client