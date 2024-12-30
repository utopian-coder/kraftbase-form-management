from sqlalchemy import create_engine
from sqlalchemy import text

from app.settings.config import settings

engine = create_engine(settings.DATABASE_URI)

NEW_DB_NAME = 'kraftbase'

with engine.connect() as conn:
    conn.execute(text("commit"))
    # Do not substitute user-supplied database names here.
    conn.execute(text(f"CREATE DATABASE {NEW_DB_NAME}"))
