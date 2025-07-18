from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PaddleOCR Service"
    PROJECT_VERSION: str = "1.0.0"

    # API V1 路由前缀
    API_V1_STR: str = "/api/v1"

    # 数据库配置
    # 格式: "mysql+mysqlconnector://user:password@host:port/dbname"
    DATABASE_URL: str

    # JWT 鉴权配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()