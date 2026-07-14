from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.supabase_client import supabase



app=FastAPI(title="Job Application tracker",version = "1.0.0")

settings=get_settings()

@app.get("/")
def root() -> dict[str,str]:
    return {
        "Message": "Application running"
    }

@app.get("/health")
def health_check()->dict[str,str]:
    return {
        "status": "healthy"
    }


@app.get("/health/supabase")
def supabase_health_check()->dict[str,str]:
    try:
        buckets=supabase.storage.list_buckets()

        bucket_exists=any(
            bucket.name == settings.supabase_storage_bucket
            for bucket in buckets

        )
        if not bucket_exists:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Supabase connection succeeded, but the "
                    "'job-documents' bucket was not found."
                ),
            )

        return {
            "status": "healthy",
            "supabase": "connected",
            "storage_bucket": settings.supabase_storage_bucket,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to Supabase.",
        ) from exc

@app.get('/health/database')
def database_health_check() -> dict[str,str|int]:
    try:
        response=(
            supabase.table('applications')
            .select("id",count='exact')
            .limit(1)
            .execute()
        )
        return {
            "status": "healthy",
            "database": "connected",
            "application_count": response.count or 0
        }   
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to query the applications table.",
        ) from exc

