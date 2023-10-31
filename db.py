from pymongo import MongoClient
from config import settings
def get_client():
    client = MongoClient(f"mongodb://{settings.user_name}:{settings.password}@{settings.host_name}", settings.port)
    return client
