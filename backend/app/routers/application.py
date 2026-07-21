from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from app.config import get_settings
from app.schemas.application import (
    ApplicationCreate,
    ApplicationDeleteResponse,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.services.application_service import (
    ApplicationNotFoundError,
    EmptyApplicationUpdateError,
    create_application,
    delete_application,
    get_application,
    list_applications,
    update_application,
)

from app.dependencies.auth import CurrentUserDependency


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"],
)

# settings = get_settings()


ApplicationId = Annotated[
    UUID,
    Path(
        description="The unique UUID of the job application.",
    ),
]


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application_endpoint(
    application: ApplicationCreate,
    current_user: CurrentUserDependency,
) -> ApplicationResponse:
    try:
        created_application = create_application(
            user_id=current_user.id,
            application=application,
        )

        return ApplicationResponse.model_validate(
            created_application
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create the application.",
        ) from exc


@router.get(
    "",
    response_model=list[ApplicationResponse],
    
)
def list_applications_endpoint(current_user: CurrentUserDependency,) -> list[ApplicationResponse]:
    try:
        applications = list_applications(
            user_id=current_user.id,
        )

        return [
            ApplicationResponse.model_validate(application)
            for application in applications
        ]

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve applications.",
        ) from exc


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application_endpoint(
    application_id: ApplicationId,
    current_user: CurrentUserDependency,
) -> ApplicationResponse:
    try:
        application = get_application(
            user_id=current_user.id,
            application_id=application_id,
        )

        return ApplicationResponse.model_validate(application)

    except ApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve the application.",
        ) from exc


@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application_endpoint(
    application_id: ApplicationId,
    application: ApplicationUpdate,
    current_user: CurrentUserDependency,
) -> ApplicationResponse:
    try:
        updated_application = update_application(
            user_id=current_user.id,
            application_id=application_id,
            application=application,
        )

        return ApplicationResponse.model_validate(
            updated_application
        )

    except EmptyApplicationUpdateError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided.",
        ) from exc

    except ApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update the application.",
        ) from exc


@router.delete(
    "/{application_id}",
    response_model=ApplicationDeleteResponse,
)
def delete_application_endpoint(
    application_id: ApplicationId,
    current_user: CurrentUserDependency,
) -> ApplicationDeleteResponse:
    try:
        delete_application(
            user_id=current_user.id,
            application_id=application_id,
        )

        return ApplicationDeleteResponse(
            message="Application deleted successfully.",
            application_id=application_id,
        )

    except ApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete the application.",
        ) from exc