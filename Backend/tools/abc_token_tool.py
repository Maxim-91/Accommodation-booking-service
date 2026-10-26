from abc import ABC, abstractmethod

from models import User


class ABCTokenTool(ABC):
    @abstractmethod
    def create_token(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError
    