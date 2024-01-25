from .database import Database


class Collection(Database):
    def __init__(self, name):
        super().__init__()
        self.collection = Database.client[Database.name][name]

    def create(self, record):
        record_id = self.collection.insert_one(
            record.db_instance()
        ).inserted_id
        return record_id
    
    def get_all(self):
        records = list(self.collection.find({}))
        return records
    
    def get_by_id(self, id):
        record = self.collection.find_one({"_id": id})
        return record