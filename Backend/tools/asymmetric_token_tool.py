import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
import uuid
import jwt
from models import User
from tools.abc_token_tool import ABCTokenTool


class AsymmetricTokenTool(ABCTokenTool):
    algorithm = "RS256"
    token_lifetime = timedelta(minutes=30)

    def _get_private_key(self) -> str:
        key_path = self._get_key_path("TOKEN_PRIVATE_KEY_PATH")
        return key_path.read_text(encoding="utf-8")

    def _get_public_key(self) -> str:
        key_path = self._get_key_path("TOKEN_PUBLIC_KEY_PATH")
        return key_path.read_text(encoding="utf-8")

    @staticmethod
    def _get_key_path(environment_variable: str) -> Path:
        key_path = os.getenv(environment_variable)

        if not key_path:
            raise RuntimeError(f"{environment_variable} is not configured")

        project_root = Path(__file__).resolve().parents[2]
        path = Path(key_path)

        if not path.is_absolute():
            path = project_root / path

        if not path.is_file():
            raise RuntimeError(f"Key file does not exist: {path}")

        return path

    def create_token(self, user: User) -> str:
        now = datetime.now(UTC)

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": now + self.token_lifetime,
        }

        return jwt.encode(
            payload,
            self._get_private_key(),
            algorithm=self.algorithm,
        )

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self._get_public_key(),
            algorithms=[self.algorithm],
            options={"require": ["sub", "iat", "exp", "jti"]},
        )
