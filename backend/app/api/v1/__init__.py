from fastapi import APIRouter
from app.api.v1.routes import auth, users, items
from .routes.listings import router as listings_router
from .routes.images import router as images_router
from .routes.categories import router as categories_router

# Root API router for version v1.
# This module aggregates and mounts all route modules under a single router.
api_router = APIRouter()

# Core application routes.
# Each module exposes its own router, which is included here.
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(items.router)

# Feature-specific routes with explicit prefixes and tags.
# These routers are defined locally withing the v1 package.
api_router.include_router(listings_router, prefix="/listings", tags=["listings"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
