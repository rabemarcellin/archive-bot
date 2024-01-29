import schedule
import time
import bcrypt
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
    
    def get_by_key(self, sender_id, key):
        note_founds = self.collection.find({"sender_id": sender_id})
       
        for note in note_founds:
            if bcrypt.checkpw(key.encode('utf-8'), note['key']):
                note_instance = NoteInstance(note_id=note['note_id'], sender_id=note['sender_id'], key=note['key'].decode('utf-8'))
                note_instance.set_id(note['_id'])
                return note_instance
    
    def get_by_noteid(self, note_id):
        note = self.collection.find({"note_id": note_id})
        note_instance = NoteInstance(note_id=note['note_id'], sender_id=note['sender_id'], key=note['key'].decode('utf-8'))
        note_instance.set_id(note['_id'])
        return note_instance
    
    def update_key(self, note_id, new_key):
        return self.collection.update_one(
            {"note_id": note_id},
            { "$set": { "key": bcrypt.hashpw(new_key.encode('utf-8'), bcrypt.gensalt())}}
        )
    
    def get_specific(self, note_id, key):
        note_founds = self.collection.find({"note_id": note_id})
       
        for note in note_founds:
            if bcrypt.checkpw(key.encode('utf-8'), note['key']):
                note_instance = NoteInstance(note_id=note['note_id'], sender_id=note['sender_id'], key=note['key'].decode('utf-8'))
                note_instance.set_id(note['_id'])
                return note_instance
       
    
    def have_changing(self):
        with self.collection.watch() as stream:
            for change in stream:
                document = change.target
                