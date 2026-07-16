from datetime import date, datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ApplicationStatus(StrEnum):
    SAVED = "SAVED"
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ONLINE_ASSESSMENT = "ONLINE_ASSESSMENT"
    RECRUITER_CALL = "RECRUITER_CALL"
    INTERVIEW = "INTERVIEW"
    FINAL_INTERVIEW = "FINAL_INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    GHOSTED = "GHOSTED"


class ApplicationResult(StrEnum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    UNSUCCESSFUL = "UNSUCCESSFUL"
    WITHDRAWN = "WITHDRAWN"
    NO_RESPONSE = "NO_RESPONSE"


class EmploymentType(StrEnum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    TEMPORARY = "TEMPORARY"
    INTERNSHIP = "INTERNSHIP"
    APPRENTICESHIP = "APPRENTICESHIP"
    FREELANCE = "FREELANCE"
    OTHER = "OTHER"


JobTitle = Annotated[
    str,
    Field(
        min_length=1,
        max_length=255,
        description="The job title for the application.",
        examples=["Data Scientist"],
    ),
]


class ApplicationBase(BaseModel):
    company_id: UUID | None = None

    job_title: JobTitle

    job_description: str | None = None
    job_url: HttpUrl | None = None
    location: str | None = Field(
        default=None,
        max_length=255,
    )
    employment_type: EmploymentType | None = None
    salary_text: str | None = Field(
        default=None,
        max_length=255,
    )

    date_applied: date

    status: ApplicationStatus = ApplicationStatus.APPLIED
    result: ApplicationResult = ApplicationResult.PENDING

    source: str | None = Field(
        default=None,
        max_length=100,
    )
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company_id: UUID | None = None

    job_title: JobTitle | None = None

    job_description: str | None = None
    job_url: HttpUrl | None = None
    location: str | None = Field(
        default=None,
        max_length=255,
    )
    employment_type: EmploymentType | None = None
    salary_text: str | None = Field(
        default=None,
        max_length=255,
    )

    date_applied: date | None = None

    status: ApplicationStatus | None = None
    result: ApplicationResult | None = None

    source: str | None = Field(
        default=None,
        max_length=100,
    )
    notes: str | None = None


class ApplicationResponse(ApplicationBase):
    id: UUID
    application_number: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationDeleteResponse(BaseModel):
    message: str
    application_id: UUID