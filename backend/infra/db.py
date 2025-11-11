"""
数据库orm连接
"""
import os
import json
import logging
from contextlib import contextmanager
from typing import Any, Optional

from sqlalchemy import Dialect, create_engine, types
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.sql.type_api import _T

from config import DATA_PATH, DB_TYPE

log = logging.getLogger(__name__)

class JSONField(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)

if DB_TYPE == "mysql":
    # 数据库连接初始化
    print("使用mysql作为数据库")
    username = "utcssc"
    password = "UTCsoft_1234"
    host="localhost:33060"
    database="tender_data"
    
    DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"
else:
    print("使用sqlite作为数据库")
    DATABASE_URL = os.getenv("SQLITE_URL", f"sqlite:///{str(DATA_PATH)}/test.db")


engine = create_engine(DATABASE_URL, json_serializer=lambda obj: json.dumps(obj,ensure_ascii=False))

SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
        )

Base = declarative_base()
Session = scoped_session(SessionLocal)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db = contextmanager(get_session)
