from fastapi import APIRouter
from app.api.v1.routes import auth, users
from .routes.listings import router as listings_router
from .routes.images import router as images_router
from .routes.categories import router as categories_router
from .routes.transaction import router as transactions_router

# Main API router for version v1
api_router = APIRouter()

# Core routes
api_router.include_router(auth.router)
api_router.include_router(users.router)

# Feature routes
api_router.include_router(listings_router, prefix="/listings", tags=["listings"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
