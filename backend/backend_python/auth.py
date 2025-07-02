from fastapi import HTTPException, Request, Depends
from pydantic import BaseModel
from pymongo.collection import Collection
import bcrypt
from jose import JWTError, jwt
import datetime
from backend_python.models import LoginUser, RegisterUser

# Secret y algoritmo
SECRET_KEY = "clave_super_secreta"  # ¡Cámbiala por algo seguro!
ALGORITHM = "HS256"

# ⏳ Duración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 día

# 🔐 Hashea contraseña
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# ✅ Verifica contraseña
def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

# 🔑 Crea token JWT
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 👤 Obtiene usuario desde token
def get_current_user(request: Request) -> str:
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# 📋 Registro de usuario
def register_user(user: RegisterUser, users_collection: Collection):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    hashed_pw = hash_password(user.password)
    users_collection.insert_one({
        "username": user.username,
        "password": hashed_pw,
        "balance": user.balance
    })
    return {"message": "Usuario registrado con éxito"}

# 🔐 Login
def login_user(user: LoginUser, users_collection: Collection):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token}
