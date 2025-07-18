from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

def now_utc():
    return datetime.now(timezone.utc)

class Client(Base):
    __tablename__ = "oauth_clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), unique=True, index=True, nullable=False, comment="客户端ID")
    hashed_secret = Column(String(255), nullable=False, comment="加密后的客户端密钥")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=now_utc, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc, nullable=False, comment="更新时间")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    token_version = Column(Integer, default=0, nullable=False, comment="token版本号，用于强制失效token")

class Token(Base):
    __tablename__ = "oauth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), ForeignKey("oauth_clients.client_id"), nullable=False, index=True, comment="客户端ID")
    token = Column(String(512), nullable=False, unique=True, index=True, comment="JWT Token")
    issued_at = Column(DateTime, default=now_utc, nullable=False, comment="签发时间")
    expires_at = Column(DateTime, nullable=False, comment="过期时间")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否有效")
    revoked_at = Column(DateTime, nullable=True, comment="注销时间")
    ip = Column(String(64), nullable=True, comment="签发时IP")
    user_agent = Column(String(256), nullable=True, comment="签发时User-Agent")