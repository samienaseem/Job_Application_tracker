from fastapi import APIRouter, HTTPException, status

from app.dependencies.auth import CurrentUserDependency
from app.schemas.auth import (
    CurrentUser,
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import (
    InvalidLoginError,
    MissingAuthSessionError,
    login_user,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_endpoint(
    login_request: LoginRequest,
) -> TokenResponse:
    try:
        return login_user(
            login_request=login_request,
        )

    except InvalidLoginError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except MissingAuthSessionError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase did not return an authentication session.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete login.",
        ) from exc


@router.get(
    "/me",
    response_model=CurrentUser,
)
def get_current_user_endpoint(
    current_user: CurrentUserDependency,
) -> CurrentUser:
    return current_user