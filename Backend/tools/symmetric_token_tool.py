from datetime import UTC, datetime, timedelta
import os
import uuid

import jwt

from models import User
from tools.abc_token_tool import ABCTokenTool


class SymmetricTokenTool(ABCTokenTool):
    algorithm = "HS512"
    token_lifetime = timedelta(minutes=30)

    def _get_key(self) -> str:
        key = os.getenv("TOKEN_KEY")

        if not key:
            raise RuntimeError("TOKEN_KEY is not configured")

        return key

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
            self._get_key(),
            algorithm=self.algorithm,
        )

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self._get_key(),
            algorithms=[self.algorithm],
            options={"require": ["sub", "iat", "exp", "jti"]},
        )
