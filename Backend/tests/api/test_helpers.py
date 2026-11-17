import os
from pathlib import Path

# database.py creates its engine at import time, so set a harmless test URL first.
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("TOKEN_KEY", "api-tests-only-secret-key-change-me")

import sys
BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database import get_db
from main import app
from tests.unit.test_helpers import create_test_session


class ApiTestCaseMixin:
    def setUp(self):
        self.engine, self.session = create_test_session()

        def override_get_db():
            try:
                yield self.session
            finally:
                pass

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.session.close()
        self.engine.dispose()
