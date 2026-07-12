from app.config import get_settings


settings = get_settings()

print("Application name:", settings.app_name)
print("Environment:", settings.app_env)
print("Debug:", settings.debug)
print("Supabase URL:", settings.supabase_url)
print("Storage bucket:", settings.supabase_storage_bucket)
print("Supabase secret loaded:", bool(settings.supabase_secret_key))
print("Supabase secret loaded:", settings.model_config)