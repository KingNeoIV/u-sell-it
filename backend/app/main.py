from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1 import api_router
from app.core.config import settings

# Create the FastAPI app once
app = FastAPI(title=settings.app_name)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
