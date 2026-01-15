from fastapi import APIRouter

# Router for item-related endpoints.
# All routes in this module are grouped under /items.
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def list_items():
    """
    Return a list of items.

    This is a placeholder endpoint. Replace the static return value
    with real data once item functionality is implemented.
    """
    return []
