from pydantic import BaseModel

class ClientBase(BaseModel):
    client_id: str

class ClientCreate(ClientBase):
    client_secret: str

class Client(ClientBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True