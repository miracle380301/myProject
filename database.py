from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# SQLite 데이터베이스 연결
DATABASE_URL = "postgresql+psycopg2://miracle:qMlgWCFKScKuyiprqBP6IUyhZF4RTclZ@dpg-cvh4p7qn91rc73atcdvg-a.oregon-postgres.render.com/crypto_1fhp"
engine = create_engine(DATABASE_URL, echo=True)
 
# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# Define Base class
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()