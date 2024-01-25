import schedule
import time
from schemas.noteinstance import NoteInstance
from .collection import Collection


class NoteInstanceModel(Collection):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def create(self, note: NoteInstance):
        note_instance_id = self.collection.insert_one(
            note.db_instance()
        ).inserted_id
        return note_instance_id
    
    def get_by_key(self, key):
        db_note = self.collection.find_one({"text_alias": key})
        note_instance = NoteInstance(note_id=db_note['note_id'], text_alias=db_note["text_alias"])
        note_instance.set_id(db_note['_id'])
        return note_instance
    
    def have_changing(self):
        with self.collection.watch() as stream:
            for change in stream:
                document = change.target
                