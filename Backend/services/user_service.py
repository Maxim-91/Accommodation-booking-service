import jwt
from passlib.hash import argon2
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from models import User
from tools.abc_token_tool import ABCTokenTool


class UserService:
    def __init__(
        self,
        repository: Session,
        token_tool: ABCTokenTool,
    ) -> None:
        self._repository = repository
        self._token_tool = token_tool

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self._repository.scalars(statement).first()

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
    ) -> User:
        normalized_email = email.strip().lower()

        if self.get_by_email(normalized_email) is not None:
            raise ConflictException("Email is already registered")

        password_hash = argon2.hash(password)

        user = User(
            full_name=full_name.strip(),
            email=normalized_email,
            password_hash=password_hash,
        )

        try:
            self._repository.add(user)
            self._repository.commit()
            self._repository.refresh(user)
            return user
        except IntegrityError as error:
            self._repository.rollback()

            # A unique database constraint provides additional protection against
            # simultaneous registration requests for the same email
            raise ConflictException(
                "Email is already registered"
            ) from error
        except Exception:
            self._repository.rollback()
            raise

    def login(self, email: str, password: str) -> str:
        normalized_email = email.strip().lower()
        user = self.get_by_email(normalized_email)

        if user is None:
            raise UnauthorizedException("Invalid email or password")

        try:
            password_is_valid = argon2.verify(
                password,
                user.password_hash,
            )
        except (TypeError, ValueError):
            password_is_valid = False

        if not password_is_valid:
            raise UnauthorizedException("Invalid email or password")

        return self._token_tool.create_token(user)

    def get_user_by_access_token(self, access_token: str) -> User | None:
        try:
            payload = self._token_tool.decode_token(access_token)
            user_id = int(payload["sub"])
        except (jwt.PyJWTError, KeyError, TypeError, ValueError):
            return None

        statement = select(User).where(User.id == user_id)
        return self._repository.scalars(statement).first()
