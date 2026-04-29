from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1 import api_router
from app.core.config import settings

# Create the FastAPI app once
app = FastAPI(title=settings.app_name)

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded images as static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all versioned API routes
app.include_router(api_router)

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "u-sell-it API is running"}
