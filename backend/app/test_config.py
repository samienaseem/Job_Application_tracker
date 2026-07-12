from app.config import get_settings
from supabase import create_client


settings = get_settings()

print("Application name:", settings.app_name)
print("Environment:", settings.app_env)
print("Debug:", settings.debug)
print("Supabase URL:", settings.supabase_url)
print("Storage bucket:", settings.supabase_storage_bucket)
print("Supabase secret loaded:", bool(settings.supabase_secret_key))
print("Supabase secret loaded:", settings.model_config)

print("Creating Supabase client...")

supabase = create_client(settings.supabase_url, settings.supabase_secret_key)

print("Client created successfully",supabase)

buckets=supabase.storage.list_buckets()
print("Buckets Name",buckets)