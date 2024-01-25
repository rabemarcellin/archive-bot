from bson.objectid import ObjectId
from datetime import datetime


class NoteInstance:
    # note instance is deprecated if is passed 15 days and no call from any app user
    # means it will be deleted
    __is_deprecated = False

    def __init__(self, note_id: ObjectId, text_alias: str) -> None:
        self.note_id = note_id
        self.text_alias = text_alias
        self.last_call = datetime.now()

    def set_id(self, id):
        self.__id = id
        
    def db_instance(self) -> dict:
        return {
            "note_id": self.note_id,
            "text_alias": self.text_alias
        }

    def have_change(self):
        ...

    def run_call_eventlistener(self):
        ...