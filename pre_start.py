import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine, SessionLocal
from app.models.client import Client
from app.core.security import get_password_hash
from app.crud.crud_client import get_client_by_client_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = "ocr_client"
CLIENT_SECRET = "ocr_client_secret"

def test_db_connection():
    """测试数据库连接。"""
    try:
        connection = engine.connect()
        logger.info("数据库连接成功！")
        connection.close()
        return True
    except SQLAlchemyError as e:
        logger.error(f"数据库连接失败: {e}")
        return False

def init_db(db: Session) -> None:
    try:
        logger.info("正在尝试创建数据库表...")
        Client.metadata.create_all(bind=engine)
        logger.info("数据库表创建（或检查）完成。")

        client = get_client_by_client_id(db, client_id=CLIENT_ID)
        if not client:
            logger.info(f"正在创建默认客户端: {CLIENT_ID}")
            hashed_secret = get_password_hash(CLIENT_SECRET)
            client_in = Client(
                client_id=CLIENT_ID,
                hashed_secret=hashed_secret,
                is_active=True
            )
            db.add(client_in)
            db.commit()
            db.refresh(client_in)
            logger.info("默认客户端创建成功。")
        else:
            logger.info("默认客户端已存在，跳过创建。")
    except SQLAlchemyError as e:
        logger.error(f"在数据库初始化过程中发生错误: {e}")
        db.rollback() # 如果出错则回滚

def main() -> None:
    logger.info("开始服务初始化...")
    if test_db_connection():
        db = SessionLocal()
        init_db(db)
        db.close()
    logger.info("服务初始化结束。")

if __name__ == "__main__":
    main()