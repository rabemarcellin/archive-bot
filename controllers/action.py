import ampalibe
import rapidfuzz
import jwt
from datetime import datetime, timedelta
from datas import actions, commands
from utils import get_sentence
from bson import ObjectId
from schemas.note import Note
from schemas.noteinstance import NoteInstance
from views import main as mainview
import views.action as actionview
from views.action import send_options
from globalinstance import chat, fake, query, data_search_center, note_model, note_instance_model
from views.template import render_note_items
from .helper import NoteQuery

notequery = None
note_id = None

@ampalibe.action(actions["research"])
@mainview.render
def research(sender_id, cmd, **ext):
    keysearch = cmd
    search_results = rapidfuzz.process.extract(keysearch, data_search_center)
    selected_notes = [
        note_model.get_by_title(title) 
        for (title, match_in_percent, search_index) 
        in search_results 
        if match_in_percent > 50
    ]
    if len(selected_notes) == 0:
        chat.send_text(sender_id, get_sentence("SEARCH_NOT_FOUND"))
        send_options(
            sender_id, 
            options=["research", "cancel"]
        )
    else:
        render_note_items(sender_id, notes=selected_notes)
        # todo: send default  options. retourner au menu principal
        send_options(sender_id, default=True)

@ampalibe.action(actions["prompt note"])
@mainview.render
def prompt_note(sender_id, cmd, **ext):
    key = cmd
    note_instance = note_instance_model.get_by_key(sender_id, key)
    # todo: render note
    if not note_instance:
        chat.send_text(sender_id, get_sentence("search not found"))
        send_options(sender_id, options=["research", "cancel"])
    else:
        mainview.render_note(sender_id, note_instance.note_id)

    # todo: update last time call registered of the note
    note_instance.last_call = datetime.now()

@ampalibe.action(actions["register note"])
@mainview.render
def register_note(sender_id, cmd, **ext):
    global notequery
    global note_id
    if  notequery.ready_for_operation():
        # insert in db
        note = Note(notequery.title, notequery.source_ref, notequery.records)
        note_id = note_model.create(note)
        # tell user note created, ask here the key used for reached the note. 
        #todo: give options if user wanna enter their own key or ok for random
        actionview.generate_key_options(sender_id)


@ampalibe.action(actions["generate key"])
@mainview.render
def generate_key(sender_id, cmd, **ext):
    global note_id
    key = None
    
    #todo: verify if key is already use for referencing existing note
    if cmd != commands["generate random key"]:
        key = cmd
        is_key_exists = note_instance_model.get_by_key(sender_id, key)
        if is_key_exists:
            chat.send_text(sender_id, "Cette clé est déjà utilisé pour une autre note")
            chat.send_text(sender_id, 'Inserer un autre clé: ')
            query.set_action(sender_id, actions["generate key"])
            return None
    else:
        key = fake.nic_handle()
        is_key_exists = note_instance_model.get_by_key(sender_id, key)
        while is_key_exists:
            key = fake.domain_word()
            is_key_exists = note_instance_model.get_by_key(sender_id, key)

    note_instance = NoteInstance(note_id=note_id , sender_id=sender_id, key=key)
    note_instance_model.create(note_instance)

    if cmd == commands["generate random key"]:
        chat.send_text(sender_id, "voici votre clé: ")
        chat.send_text(sender_id, key)

    chat.send_text(sender_id, "Surtout ne le perdez pas!")

    # todo: give right way options after creating something.
    # creating an other, retour au main
    send_options(sender_id, options=["create another note", "go main menu"])
    query.set_action(sender_id, actions["create note"])

@ampalibe.action(actions["create note"])
@mainview.render
def create_note(sender_id, cmd, **ext):
    global notequery
    notequery = NoteQuery(sender_id)
    actionview.prompt_title(sender_id, notequery)
    
@ampalibe.action(actions["prompt title"])
@mainview.render
def prompt_title(sender_id, cmd, **ext):
    global notequery
    notequery.title = cmd
    actionview.prompt_source_ref(sender_id, notequery)

@ampalibe.action(actions["prompt source ref"])
@mainview.render
def prompt_source_ref(sender_id, cmd, **ext):
    global notequery
    notequery.source_ref = cmd
    actionview.prompt_records(sender_id, notequery)

@ampalibe.action(actions["prompt records"])
@mainview.render
def prompt_records(sender_id, cmd, **ext):
    global notequery
    if cmd == commands["end records"]:
        notequery.is_finish = True
    if not notequery.is_finish:
        notequery.records.append(cmd)
        actionview.prompt_records(sender_id, notequery)
    else:
        send_options(sender_id, options=["register note", "cancel"])
        query.set_action(sender_id, actions["register note"])


@ampalibe.action(actions["prompt new key"])
@mainview.render
def prompt_new_key(sender_id, cmd, **ext):
    secret = query.get_temp(sender_id, 'secret')
    token = query.get_temp(sender_id, 'token')
    query.set_temp(sender_id, 'new_key', cmd)
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        send_options(sender_id, options=["update key", "reedit key", "cancel"])
    except jwt.ExpiredSignatureError:
        chat.send_text(sender_id, "Délais d'attente un peu long, veuillez réessayer")
        send_options(sender_id, options=["edit key", "cancel"])
   

@ampalibe.action(actions["edit key"])
@mainview.render
def edit_key(sender_id, cmd, **ext):
    secret = query.get_temp(sender_id, 'secret')
    token = query.get_temp(sender_id, 'token')
    try:
        key = cmd
        print(token)
        print(secret)
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        note_id = payload["note_id"]
        print(note_id)
        is_key_exists = note_instance_model.get_specific(ObjectId(note_id), key)
        if is_key_exists:
            chat.send_text(sender_id, "Entrer la nouvelle clé: ")
            query.set_action(sender_id, actions["prompt new key"])
        else:
            chat.send_text(sender_id, "Clé incorrect.")
            send_options(sender_id, options=["edit key", "cancel"])

    except jwt.ExpiredSignatureError:
        chat.send_text(sender_id, "Délais d'attente un peu long, veuillez réessayer")
        send_options(sender_id, options=["edit key", "cancel"])


        


