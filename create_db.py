from sqlalchemy import create_engine
from sqlalchemy import text

from app.settings.config import settings

if settings.LOCAL:
    admin_url = "postgresql://postgres:root@localhost:5432/postgres"
else:
    admin_url = "postgresql://postgres:root@postgres:5432/postgres"

engine = create_engine(admin_url)

NEW_DB_NAME = 'kraftbase'

with engine.connect() as conn:
    conn.execute(text("commit"))
    # Do not substitute user-supplied database names here.
    conn.execute(text(f"CREATE DATABASE {NEW_DB_NAME}"))
