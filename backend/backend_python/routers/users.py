from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection
from backend_python.auth import (
    UserIn,
    register_user,
    login_user,
    get_current_user
)
from backend_python.database import users_collection

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register")
def register(user: UserIn):
    return register_user(user, users_collection)

@router.post("/login")
def login(user: UserIn):
    return login_user(user, users_collection)

@router.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username}
