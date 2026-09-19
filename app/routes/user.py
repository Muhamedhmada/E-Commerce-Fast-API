from fastapi import APIRouter
from app.services.user import get_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user_endpoint(user_id: int):
    return get_user(user_id)