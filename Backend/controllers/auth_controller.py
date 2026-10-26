from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from dtos.login import LoginRequest, LoginResponse
from dtos.registration import RegistrationRequest, RegistrationResponse
from factories.services import user_service_factory
from services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Creating a dependency type for a service
UserServiceDep = Annotated[UserService, Depends(user_service_factory)]


@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register_user(
    request: RegistrationRequest,
    service: UserServiceDep,
) -> RegistrationResponse:
    try:
        user = service.register(
            full_name=request.full_name,
            email=str(request.email),
            password=request.password,
        )
        return user
    except ConflictException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
)
def login_user(
    request: LoginRequest,
    service: UserServiceDep,
) -> LoginResponse:
    try:
        token = service.login(
            email=str(request.email),
            password=request.password,
        )
        return LoginResponse(access_token=token)
    except UnauthorizedException as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
