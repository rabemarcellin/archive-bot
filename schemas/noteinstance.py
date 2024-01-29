import jwt
import bcrypt
from datetime import datetime as dt, timedelta


class NoteInstance:
    # note instance is deprecated if is passed 15 days and no call from any app user
    # means it will be deleted
    __delay_expiration = 15

    def __init__(self, note_id, sender_id: int, key: str) -> None:
        self.note_id = note_id
        self.sender_id = sender_id
        self.key = bcrypt.hashpw(key.encode('utf-8'), bcrypt.gensalt())
        self.iat = dt.now()
#        self.iat = current_datetime + timedelta(minutes=self.__delay_expiration) # assign 15 min delay expiration for this note
 
    def set_id(self, id):
        self.__id = id
        
    def db_instance(self) -> dict:
        note_instance = {
            "note_id": self.note_id, 
            "sender_id": self.sender_id, 
            "key": self.key,
            "iat": self.iat, 
        }
        return note_instance
    
    def have_change(self):
        ...

    def run_call_eventlistener(self):
        ...