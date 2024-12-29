from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)  # fetch db env from env
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DB:
  def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = DB()
