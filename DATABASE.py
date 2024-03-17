from appConfig import *
from pymongo import MongoClient


class DATABASE():
    client = None

    def __init__(self):
        self._initialize_mongodb_client()

    def _initialize_mongodb_client(self):
        if DATABASE.client is None:
            DATABASE.client = MongoClient(ENV_VAR.MONGO_DB_URL)
