from .collection import Collection
from schemas.note import Note


class NoteModel(Collection):
    def __init__(self, collection_name):
        super().__init__(collection_name)

    def create(self, note: Note):
        note_id = self.collection.insert_one(
            note.db_instance()
        ).inserted_id
        return note_id
    
    def get_by_title(self, title) -> Note:
        db_note = self.collection.find_one({"title": title})
        note = Note(title=db_note['title'], source_ref=db_note['source_ref'], records=db_note['records'])
        note.set_id(db_note._id)
        return note
        