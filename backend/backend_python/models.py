from pydantic import BaseModel


    
class RegisterUser(BaseModel):
    username: str
    password: str
    balance: float

class LoginUser(BaseModel):
    username: str
    password: str
    
class BalanceUpdate(BaseModel):
    balance: float