from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings

# Main FastAPI application instance.
# The app name is pulled from the configuration for consistency across environmets.
app = FastAPI(title=settings.app_name)

# Include all versioned API routes.
app.include_router(api_router)


# Health check endpoint to confirm the API is running.
@app.get("/")
def read_root():
    return {"message": "u-sell-it API is running"}
