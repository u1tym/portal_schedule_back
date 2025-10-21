import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

# スケジュール用データベース設定
SCHEDULE_DATABASE_URL = os.getenv("SCHEDULE_DATABASE_URL", "postgresql://puser:ppassword@localhost:5432/portal?client_encoding=utf8")

# スケジュール用エンジンとセッション
schedule_engine = create_engine(
    SCHEDULE_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
ScheduleSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=schedule_engine)

# スケジュール用Baseクラス
ScheduleBase = declarative_base()

def get_schedule_db() -> Generator:
    """スケジュール用データベースセッションを取得"""
    db = ScheduleSessionLocal()
    try:
        yield db
    finally:
        db.close()