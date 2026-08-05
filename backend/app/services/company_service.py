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


def get_or_create_company(*,user_id:UUID, company:CompanyInput)->dict[str,Any]:

    existing_company=find_company_by_name(user_id=user_id,company_name=company.name)

    if existing_company is not None:
        return enrich_existing_company(user_id=user_id, existing_company=existing_company, company_input=company)
    
    company_data=company.model_dump(mode="json")

    company_data['user_id']=str(user_id)

    try:
        response=(
            supabase_admin
            .table("companies")
            .insert(company_data)
            .select(COMPANY_COLUMNS)
            .execute()
            )
    except Exception as exc:
        if is_duplicate_company_error(exc):
            existing_company = find_company_by_name(user_id=user_id,company_name=company.name)

        if existing_company is not None:
            return existing_company
    
        raise

    if not response.data:
        raise RuntimeError("Supabase did not return the company")
    
    return response.data[0]


def enrich_existing_company(*, user_id:UUID, existing_company:dict[str,Any], company:CompanyInput)->dict[str,Any]:
    update_data:dict[str,Any]={}

    if  not existing_company.get('website') and company.websiteUrl is not None:
        update_data['website']=str(company.websiteUrl)
    
    if (
        not existing_company.get("location")
        and company_input.location is not None
    ):
        update_data["location"] = (
            company_input.location
        )

    if not update_data:
        return existing_company
    

    response=(
        supabase_admin.table("companies")
        .update(update_data)
        .eq(user_id,str(user_id))
        .eq(id,existing_company["id"])
        .select(COMPANY_COLUMNS)
        .execute()
    )
    if not response.data:
        return existing_company
    
    return response.data[0]


def list_companies_with_application_count(*,user_id:UUID) -> list(dict[str,Any]):


    companies_response=(
        supabase_admin.table("companies")
        .select(COMPANY_COLUMNS)
        .eq(user_id, str(user_id))
        .order("name")
        .execute()
    )

    Application_response=(
        supabase_admin.table("applications")
        .select("company_id")
        .eq(user_id, str(user_id))
        .execute()
    )

#     company_counts = {}
# for row in applications_response.data:
#     cid = row.get("company_id")
#     if cid is not None:
#         if cid in company_counts:
#             company_counts[cid] += 1
#         else:
#             company_counts[cid] = 1

    companies_count = Counter(
        row['company_id'] for row in Application_response.data if row.get("company_id") is not None
    )
    # company_count = {"company_id_1": 3, "company_id 2": 2}

    company_items:list(dict[str,Any]) = []
    
    for company in companies_response.data:
        application_count = companies_count.get(company['id'],0)

        if application_count == 0:
            continue

        company_items.append(
            "id": company['id'],
            "name": company['name'],
            "website": company['website'],
            "location": company['location'],
            "application_count": application_count
        )

    return company_items

def delete_company_if_unused(
    *,
    user_id: UUID,
    company_id: UUID,
) -> None:
    applications_response = (
        supabase_admin
        .table("applications")
        .select("id")
        .eq("company_id", str(company_id))
        .eq("user_id", str(user_id))
        .limit(1)
        .execute()
    )

    if applications_response.data:
        return

    (
        supabase_admin
        .table("companies")
        .delete()
        .eq("id", str(company_id))
        .eq("user_id", str(user_id))
        .execute()
    )



def is_duplicate_company_error(execption:Exception)-> bool:
    error_text = str(exception).lower()

    return (
        "companies_user_name_unique_idx"
        in error_text
        or "duplicate key value"
        in error_text
    )

