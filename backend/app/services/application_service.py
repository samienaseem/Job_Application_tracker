from typing import Any
from uuid import UUID

from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
)
from app.supabase_client import supabase_admin


APPLICATION_COLUMNS = """
    id,
    application_number,
    user_id,
    company_id,
    job_title,
    job_description,
    job_url,
    location,
    employment_type,
    salary_text,
    date_applied,
    status,
    result,
    source,
    notes,
    created_at,
    updated_at
"""


class ApplicationNotFoundError(Exception):
    """Raised when an application does not exist for the given user."""


class EmptyApplicationUpdateError(Exception):
    """Raised when an update request contains no fields."""


def create_application(
    *,
    user_id: UUID,
    application: ApplicationCreate,
) -> dict[str, Any]:
    application_data = application.model_dump(
        mode="json",
    )

    application_data["user_id"] = str(user_id)

    response = (
        supabase
        .table("applications")
        .insert(application_data)
        .select(APPLICATION_COLUMNS)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Supabase did not return the created application."
        )

    return response.data[0]


def list_applications(
    *,
    user_id: UUID,
) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("applications")
        .select(APPLICATION_COLUMNS)
        .eq("user_id", str(user_id))
        .order("date_applied", desc=True)
        .execute()
    )

    return response.data


def get_application(
    *,
    user_id: UUID,
    application_id: UUID,
) -> dict[str, Any]:
    response = (
        supabase_admin    
        .table("applications")
        .select(APPLICATION_COLUMNS)
        .eq("id", str(application_id))
        .eq("user_id", str(user_id))
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ApplicationNotFoundError

    return response.data[0]


def update_application(
    *,
    user_id: UUID,
    application_id: UUID,
    application: ApplicationUpdate,
) -> dict[str, Any]:
    update_data = application.model_dump(
        mode="json",
        exclude_unset=True,
    )

    if not update_data:
        raise EmptyApplicationUpdateError

    response = (
        supabase_admin
        .table("applications")
        .update(update_data)
        .eq("id", str(application_id))
        .eq("user_id", str(user_id))
        .select(APPLICATION_COLUMNS)
        .execute()
    )

    if not response.data:
        raise ApplicationNotFoundError

    return response.data[0]


def delete_application(
    *,
    user_id: UUID,
    application_id: UUID,
) -> None:
    existing_application = get_application(
        user_id=user_id,
        application_id=application_id,
    )
# for update
    response = (
        supabase_admin
        .table("applications")
        .delete()
        .eq("id", str(existing_application["id"]))
        .eq("user_id", str(user_id))
        .execute()
    )

    if not response.data:
        raise ApplicationNotFoundError