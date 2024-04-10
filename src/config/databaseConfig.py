from src.config.appConfig import *
from pymongo import MongoClient


class DATABASE:
    client = None
    collections=None
    def __init__(self):
        self._initialize_mongodb_client()

    def _initialize_mongodb_client(self):
        if DATABASE.client is None:
            DATABASE.client = MongoClient(ENV_VAR.MONGO_DB_URL)
            print("mongodb connected")

            # print(
            #     DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chathistories"].find_one(
            #         {"username": "dhruv4023","history": {"_id": "65f326753dee7ed79642f306"}}
            #     )
            # )