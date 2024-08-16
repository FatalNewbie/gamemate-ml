# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 읽기
db_url = os.getenv("DB_URL")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

DATABASE_URL =f"mysql+pymysql://{db_user}:{db_password}@{db_url}:3306/gamemate"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

