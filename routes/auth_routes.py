
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.user import (
    UserRegister,
    UserResponseMessage,
    TokenResponse
)

from database import (
    insert_user,
    fetch_user_by_username
)

from security import (
    hash_password,
    verify_password,
    create_access_token
)

from dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# REGISTER USER
@router.post(
    "/register",
    response_model=UserResponseMessage,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserRegister):

    existing_user = fetch_user_by_username(user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    try:
        user_id = insert_user(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role="Receptionist"
        )

        return {
            "message": "User registered successfully",
            "user": {
                "user_id": user_id,
                "username": user.username,
                "email": user.email,
                "role": "Receptionist"
            }
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )


# LOGIN USER
@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    existing_user = fetch_user_by_username(form_data.username)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(
        form_data.password,
        existing_user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={
            "sub": str(existing_user["user_id"])
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# GET CURRENT USER
@router.get("/me")
def get_my_profile(
    current_user=Depends(get_current_user)
):

    return {
        "message": "User profile retrieved successfully",
        "user": {
            "user_id": current_user["user_id"],
            "username": current_user["username"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    }
