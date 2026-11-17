import os
from pathlib import Path
import sys

# database.py requires DATABASE_URL at import time. Integration migrations use TEST_DATABASE_URL.
os.environ.setdefault("DATABASE_URL", os.getenv("TEST_DATABASE_URL") or "sqlite+pysqlite:///:memory:")

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def get_test_database_url():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        return None
    if not url.startswith(("postgresql://", "postgresql+psycopg://")):
        raise RuntimeError("TEST_DATABASE_URL must point to a dedicated PostgreSQL test database.")
    return url


def create_migrated_test_database():
    url = get_test_database_url()
    if not url:
        raise RuntimeError("Set TEST_DATABASE_URL to a dedicated PostgreSQL test database.")

    # migrations/env.py reads DATABASE_URL. Set it only for this test process.
    os.environ["DATABASE_URL"] = url
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    command.upgrade(config, "head")

    engine = create_engine(url, pool_pre_ping=True)
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, session_local
