import logging
from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal  # 导入 SessionLocal
from pre_start import test_db_connection, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json"  # 注释掉自定义openapi_url
    # 保持默认即可，docs和redoc才能正常
)

@app.on_event("startup")
async def startup_event():
    logger.info("开始执行 startup 事件...")
    logger.info("正在测试数据库连接...")
    if test_db_connection():
        logger.info("数据库连接成功，正在初始化数据库...")
        db = SessionLocal()
        init_db(db)
        db.close()
        logger.info("数据库初始化完成。")
    else:
        logger.error("数据库连接失败，请检查配置和网络。")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to PaddleOCR Service"}