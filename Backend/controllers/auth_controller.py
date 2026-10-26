from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from custom_exceptions.conflict_exception import ConflictException
from dtos.registration import (
    RegistrationRequest,
    RegistrationResponse,
)
from factories.services import user_service_factory
from services.user_service import UserService


router = APIRouter(prefix="/api/auth", tags=["authentication"])

UserServ = Annotated[
    UserService,
    Depends(user_service_factory),
]


@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegistrationRequest,
    service: UserServ,
) -> RegistrationResponse:
    try:
        return service.register(
            full_name=request.full_name,
            email=str(request.email),
            password=request.password,
        )
    except ConflictException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
