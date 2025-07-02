from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["trading_app"]
users_collection = db["users"]
closed_trades_collection = db["closed_trades"]