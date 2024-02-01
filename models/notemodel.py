from bson import ObjectId
from typing import Tuple
from .collection import Collection
from schemas.note import Note


class NoteModel(Collection):
    def __init__(self, collection_name):
        super().__init__(collection_name)

    def get_all(self):
        notes = super().get_all()
        return [Note(title=db_note['title'], source_ref=db_note['source_ref'], records=db_note['records']).set_id(db_note['_id']) for db_note in notes]


    def create(self, note: Note):
        note_id = self.collection.insert_one(
            note.db_instance()
        ).inserted_id
        return note_id
    
    def get_by_id(self, id) -> Note:
        note_dict = self.collection.find_one({"_id": ObjectId(id)})
        note = Note(title=note_dict['title'], source_ref=note_dict['source_ref'], records=note_dict['records'])
        note.set_id(note_dict['_id'])
        return note
    
    def get_user_libraries(self, note_ids: Tuple[str]) -> Tuple[Note]:
        user_notes = [self.get_by_id(note_id) for note_id in note_ids]
        return tuple(user_notes)

    def get_by_title(self, title) -> Note:
        db_note = self.collection.find_one({"title": title})
        note = Note(title=db_note['title'], source_ref=db_note['source_ref'], records=db_note['records'])
        note.set_id(db_note._id)
        return note
        