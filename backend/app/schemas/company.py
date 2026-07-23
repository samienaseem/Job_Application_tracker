from pydantic import (
    BaseModel, Field, HttpUrl, field_validator,
)
from uuid import UUID
from typing import Annotated

class CompanyInput(BaseModel):
