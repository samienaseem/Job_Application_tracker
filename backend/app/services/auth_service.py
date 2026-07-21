from app.schemas.auth import LoginRequest, TokenResponse
from app.supabase_client import create_auth_client


class InvalidLoginError(Exception):
    """Raised when the supplied email or password is invalid."""


class MissingAuthSessionError(Exception):
    """Raised when Supabase does not return an authentication session."""


def login_user(
    *,
    login_request: LoginRequest,
) -> TokenResponse:
    auth_client = create_auth_client()

    try:
        response = auth_client.auth.sign_in_with_password(
            {
                "email": str(login_request.email),
                "password": login_request.password,
            }
        )

    except Exception as exc:
        raise InvalidLoginError from exc

    session = response.session

    if session is None:
        raise MissingAuthSessionError

    return TokenResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        token_type=session.token_type or "bearer",
        expires_in=session.expires_in,
        expires_at=session.expires_at,
    )