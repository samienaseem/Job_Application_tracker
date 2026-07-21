from supabase import client, create_client

from app.config import get_settings

settings=get_settings()

# def create_supabase_client() -> Client:
#     return create_client(
#         settings.supabase_url,
#         settings.supabase_secret_key
#     )


def create_admin_client() -> client:
     
        # Create a trusted backend Supabase client.

        # This client uses the secret key and must never be exposed
        # to frontend or browser code.
    
    return create_client (
        settings.supabase_url,
        settings.supabase_secret_key,
    )

def create_auth_client() -> client:
    # """
    # Create a low-privilege client for authentication operations.

    # A new instance should be created for each login request so
    # authentication session state is not shared across users.
    # """
    return create_client(
        settings.supabase_url,
        settings.supabase_publishable_key,
    )

supabase_admin: client =  create_admin_client()




# we will do databse operation here