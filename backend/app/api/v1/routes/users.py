from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_current_user():
    # later: extract user from JWT
    return {"message": "current user endpoint placeholder"}
