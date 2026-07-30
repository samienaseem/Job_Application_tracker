from typing import Any
from collections import Counter
from uuid import UUID

from app.supabase_client import supabase_admin
from app.schemas.company import CompanyInput


COMPANY_COLUMNS = """
    id,
    user_id,
    name,
    website,
    location,
    created_at,
    updated_at

"""

class CompanyNotFoundError(Exception):
    """Raised when a company cannot be found for a user."""

def find_company_by_name(*, user_id:UUID, company_name:str)->dict[str,Any] | None:
    response=(
        supabase_admin.table('companies')
        .select(COMPANY_COLUMNS)
        .eq(user_id, str(user_id))
        .ilike('name',company_name)
        .maybe_single()
        .execute()
    )

    return response.data


def find_company_by_id(*, user_id:UUID, company_id:UUID)->dict[str,Any]:
    response=(
        supabase_admin.table("companies")
        .select(COMPANY_COLUMNS)
        .eq(id,str(company_id))
        .eq(user_id,str(user_id))
        .mayble_single()
        .execute()
    )
    if response.data is None:
        raise CompanyNotFoundError
    
    return response.data