from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

DATABASE_URL = "sqlite:///bujji-bus.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()