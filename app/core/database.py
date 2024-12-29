from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.config import settings

engine = create_engine(settings.DATABASE_URI)  # fetch db env from env
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DB:
  def get_db(self):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = DB()
