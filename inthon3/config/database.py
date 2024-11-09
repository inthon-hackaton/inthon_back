from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

# 환경 변수로부터 PostgreSQL 접속 정보 가져오기
db_server = os.getenv('DB_SERVER', "leaf-postgres.c5ec4esecfuq.ap-northeast-2.rds.amazonaws.com")
db_database = os.getenv('DB_DATABASE', "")
db_port = os.getenv("DB_PORT")
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv("DB_PASSWORD")

print(db_port)
# PostgreSQL 데이터베이스 URL 설정
#SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_server}:5432/{db_database}"
SQLALCHEMY_DATABASE_URL = f"postgresql://leaf_postgres:leafleaf241109@leaf-postgres.c5ec4esecfuq.ap-northeast-2.rds.amazonaws.com:5432/leaf"
# 엔진 생성
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Database connection successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

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
