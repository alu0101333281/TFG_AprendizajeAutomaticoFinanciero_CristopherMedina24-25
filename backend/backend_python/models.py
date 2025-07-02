from pydantic import BaseModel
from typing import Literal
from datetime import datetime

    
class RegisterUser(BaseModel):
    username: str
    password: str
    balance: float

class LoginUser(BaseModel):
    username: str
    password: str
    
class BalanceUpdate(BaseModel):
    balance: float
    
class ClosedTrade(BaseModel):
  side: Literal["buy", "sell"]
  entry_price: float
  exit_price: float
  volume: float
  leverage: int
  entry_time: datetime
  exit_time: datetime
  pnl: float  # Ganancia o pérdida absoluta
  roi: float  # Porcentaje de ganancia o pérdida
  symbol: str