from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection
from backend_python.auth import (
    register_user,
    login_user,
    get_current_user
)
from backend_python.database import users_collection
from backend_python.models import LoginUser, RegisterUser, BalanceUpdate
from backend_python.database import closed_trades_collection
from backend_python.models import ClosedTrade
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


@router.post("/close_trade")
def close_trade(trade: ClosedTrade, username: str = Depends(get_current_user)):
    trade_dict = trade.dict()
    trade_dict["username"] = username
    closed_trades_collection.insert_one(trade_dict)
    return {"message": "Operación guardada"}

@router.get("/closed_trades")
def get_closed_trades(username: str = Depends(get_current_user)):
    trades = list(closed_trades_collection.find({"username": username}, {"_id": 0}))
    return trades