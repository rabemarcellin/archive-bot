from os import environ as env
from pymongo import MongoClient


class Database:
    __connection_url = env.get('DB_URL')
    name = env.get('DB')
    client = MongoClient(__connection_url)