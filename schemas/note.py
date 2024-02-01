class Note:
    def __init__(self, title, source_ref, records):
        self.title = title
        self.source_ref = source_ref
        self.records = records

    def set_id(self, id):
        self._id = id
        return self
    
    def db_instance(self) -> dict:
        return {
            "title": self.title,
            "source_ref": self.source_ref,
            "records": self.records
        }