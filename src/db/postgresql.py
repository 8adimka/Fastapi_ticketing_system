from typing import Optional

from databases import Database
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from src.core.config.app_settings import get_settings

app_config = get_settings()
database: Optional[Database] = None

engine = create_engine(app_config.db.pg_dsn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()


# Функция понадобится при внедрении зависимостей
def get_postgresql(request: Request) -> Request:
    return request.state.db
