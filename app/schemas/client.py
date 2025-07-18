from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    client_id: str

class ClientCreate(ClientBase):
    client_secret: str

class Client(ClientBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
    token_version: int

    class Config:
        orm_mode = True

class TokenBase(BaseModel):
    client_id: str
    token: str
    issued_at: datetime
    expires_at: datetime
    is_active: bool
    revoked_at: Optional[datetime] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None

class TokenCreate(BaseModel):
    client_id: str
    token: str
    issued_at: datetime
    expires_at: datetime
    ip: Optional[str] = None
    user_agent: Optional[str] = None

class TokenInDB(TokenBase):
    id: int

    class Config:
        orm_mode = True