import ampalibe
import rapidfuzz
from datetime import datetime
from datas import actions, end_records_indicator
from utils import get_sentence
from schemas.note import Note
from schemas.noteinstance import NoteInstance
from views import main as mainview
import views.action as actionview
from views.action import send_options
from globalinstance import chat, query, data_search_center, note_model, note_instance_model
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
    note_instance = note_instance_model.get_by_key(key)
    # todo: render note
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
    if cmd == end_records_indicator:
        notequery.is_finish = True
    if not notequery.is_finish:
        notequery.records.append(cmd)
        actionview.prompt_records(sender_id, notequery)
    else:
        send_options(sender_id, options=["register note", "cancel"])
        query.set_action(sender_id, actions["register note"])
        
@ampalibe.action(actions["prompt key"])
@mainview.render
def prompt_key(sender_id, cmd, **ext):
    # todo : create new note instance
    global note_id
    notekey = cmd
    note_instance = NoteInstance(note_id, text_alias=notekey)
    note_instance_model.create(note_instance)

    # clear temp 
    for var_temp in ['notekey']:
        query.del_temp(sender_id, var_temp)

    # todo: give right way options after creating something.
    # creating an other, retour au main
    send_options(sender_id, options=["create another note", "go main menu"])
