from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# DB 파일 경로 설정 (기본적으로 /app/data/travel_english.db 를 사용하되, 로컬 개발을 위해 fallback 구성)
db_dir = os.environ.get("DB_DIR", "/app/data")
try:
    os.makedirs(db_dir, exist_ok=True)
except Exception:
    # 로컬 개발 환경 등 쓰기 권한이 없을 경우 fallback 경로 사용
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(db_dir, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(db_dir, 'travel_english.db')}"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 생성을 위한 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 모델의 Base 클래스
Base = declarative_base()

# DB 세션 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
