from pydantic import (
    BaseModel, Field, HttpUrl, field_validator,
)
from uuid import UUID
from typing import Annotated

class CompanyInput(BaseModel):
    name: CompanyName

    websiteUrl: HttpUrl | None = None

    location: str | None = Field(
        default=None,
        max_length=255
        
    )

    @field_validator('name')
    @classmethod
    def normalise_company_name(cls,value:str)-> str:
        normalised_name=" ".join(value.split)

        if not normalised_name:
            raise ValueError("company name cannot be blank")
        
        return normalised_name


class CompanySummary(BaseModel):
    id:UUID
    name: str
    website: HttpUrl | None = None
    location: str | None = None


class CompanyListItem(CompanySummary):
    application_count: int = Field(
        ge=1,
        description = ("NUmber of application belong to this company"),
    )
