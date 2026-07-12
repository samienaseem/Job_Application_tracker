from supabase import client, create_client

from app.config import get_settings

settings=get_settings()

def create_supabase_client() -> client:
    return create_client(
        settings.supabase_url,
        settings.supabase_secret_key
    )

supabase: client =  create_supabase_client()

# we will do databse operation here