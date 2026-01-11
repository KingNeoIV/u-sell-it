from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "u-sell-it API is running"}
