from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection
from backend_python.auth import (
    register_user,
    login_user,
    get_current_user
)
from backend_python.database import users_collection
from backend_python.models import LoginUser, RegisterUser, BalanceUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
@router.post("/register")
def register(user: RegisterUser):
    return register_user(user, users_collection)

@router.post("/login")
def login(user: LoginUser):
    return login_user(user, users_collection)

@router.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username}

@router.get("/balance")
def get_balance(username: str = Depends(get_current_user)):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"balance": user["balance"]}

from fastapi import Body

@router.post("/update_balance")
def update_balance(
    payload: BalanceUpdate = Body(...),
    username: str = Depends(get_current_user)
):
    result = users_collection.update_one(
        {"username": username},
        {"$set": {"balance": payload.balance}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el balance")
    return {"message": "Balance actualizado correctamente"}