from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from factories.services import user_service_factory
from services.user_service import UserService


bearer_scheme = HTTPBearer(auto_error=False)

UserServ = Annotated[
    UserService,
    Depends(user_service_factory),
]


def get_logged_in_user(
    authorization: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    user_service: UserServ,
):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_service.get_user_by_access_token(
        authorization.credentials
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
