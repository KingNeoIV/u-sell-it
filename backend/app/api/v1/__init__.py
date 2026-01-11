from fastapi import APIRouter
from app.api.v1.routes import auth, users, items
from .routes.listings import router as listings_router
from .routes.images import router as images_router

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(items.router)

api_router.include_router(listings_router, prefix="/listings", tags=["listings"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
