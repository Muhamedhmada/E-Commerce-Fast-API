from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.user import get_user , get_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    
    return get_user(user_id)




@router.get("")
def get_users_endpoint(current_user: dict = Depends(get_current_user)):
    return get_users()