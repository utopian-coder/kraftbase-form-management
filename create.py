from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("postgresql://postgres:root@localhost:5432/postgres")

NEW_DB_NAME = 'kraftbase'

with engine.connect() as conn:
    conn.execute(text("commit"))
    # Do not substitute user-supplied database names here.
    conn.execute(text(f"CREATE DATABASE {NEW_DB_NAME}"))
