from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

# 환경 변수로부터 PostgreSQL 접속 정보 가져오기
db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_DATABASE')
db_port = os.getenv("DB_PORT")
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv("DB_PASSWORD")

# PostgreSQL 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_server}:5432/{db_database}"

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# 세션 로컬 설정
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base 모델 선언
Base = declarative_base()


# 데이터베이스 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 테이블 생성 함수
def create_tables():
    Base.metadata.create_all(bind=engine)
