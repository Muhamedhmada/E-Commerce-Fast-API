from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.auth import SignupRequest
from app.repositories.auth import (
    get_user_by_email,
    create_user
)
import bcrypt


def signup(data: SignupRequest):

    existing_user = get_user_by_email(data.email)

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status": 409,
                "message": "Email already exists"
            }
        )

    password_hash = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user_id = create_user(
        name=data.name,
        email=data.email,
        password_hash=password_hash
    )

    return {
        "id": user_id,
        "name": data.name,
        "email": data.email
    }


def login(data):


    existing_user = get_user_by_email(data.email)

    password = existing_user["password"]

    if password:

        is_valid = bcrypt.checkpw(
            data.password.encode("utf-8"),
            password.encode("utf-8")
        )

        if not is_valid:

            return JSONResponse(
                        status_code=status.HTTP_409_CONFLICT,
                        content={
                            "status": 409,
                            "message": "Password Is Wrong"
                        }
                    )
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status": 409,
                "message": "Email Not Found"
            }
        )


    return{
        "status":200,
        "message":"welcome, you're logged in successfully"
    }
