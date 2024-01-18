from pymongo import MongoClient
from os import environ as env

DB = env.get('DB')
DB_URL = env.get('DB_URL')
COLLECTION = env.get('COLLECTION')

client = MongoClient(DB_URL)

archives = client[f"{DB}"][F"{COLLECTION}"]


def create_db_archive(title, group_source, records):
    new_archive_id = archives.insert_one({
        "title": title,
        "group_source": group_source,
        "records": records
    }).inserted_id
    return new_archive_id

def get_all_archives():
    return archives.find({})

def get_db_archive(id):
    archive = archives.find_one({"_id": id})
    return archive

def get_title_archive(title):
    archive = archives.find_one({"title": title})
    return archive



