from fastapi import APIRouter

from app.schemas.auth import SignupRequest , LoginRequest
from app.services import auth as serv


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/signup", status_code=201)
def signup_endpoint(data: SignupRequest):
    return serv.signup(data)


@router.post("/login" , status_code=201)
def login(data:LoginRequest):

    return serv.login(data)