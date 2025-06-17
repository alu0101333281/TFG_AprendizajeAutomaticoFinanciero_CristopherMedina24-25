from fastapi import FastAPI
from backend_python.database import users_collection
from fastapi.middleware.cors import CORSMiddleware
from backend_python.auth import UserIn, register_user, login_user, get_current_user
from backend_python.models import UserIn
from fastapi import Depends
from backend_python.routers import users
app = FastAPI()
import sys
import os


# Agrega la ruta raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app.include_router(users.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O específica tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/test-db")
def test_db():
    try:
        # Intenta contar documentos (no importa cuántos haya)
        count = users_collection.count_documents({})
        return {"success": True, "user_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
app.include_router(users.router)