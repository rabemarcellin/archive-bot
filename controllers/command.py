import ampalibe
import jwt
from datetime import datetime,  timedelta, timezone
from bson import ObjectId
from utils import get_sentence
from datas import commands, actions, persistent_menu, end_records_indicator
from globalinstance import chat, query, note_model, fake, note_instance_model
from views import main as mainview
import views.action as actionview
from views.action import send_options
from views.template import render_note_items


chat.get_started()

# oriented render (->)
@ampalibe.command(commands["root"])
@mainview.render
def main(sender_id, cmd, **ext):
    chat.persistent_menu(sender_id, persistent_menu)
    send_options(
        sender_id, 
        header_text=get_sentence("ROOT_OPTIONS_HEADER"), 
        options=["libraries", "get note", "create note"]
    )

# oriented render (->)
@ampalibe.command(commands["libraries"])
@mainview.render
def get_libraries(sender_id, cmd, **ext):
    user_note_ids = note_instance_model.get_users_id(sender_id)
    notes = note_model.get_user_libraries(user_note_ids)
    render_note_items(sender_id, notes)

@ampalibe.command(commands["research"])
@mainview.render
def research_note(sender_id, cmd, **ext):
    chat.send_text(sender_id,  get_sentence("INPUT_KEYSEARCH"))
    query.set_action(sender_id, actions["research"])

@ampalibe.command(commands["cancel"])
@mainview.render
def cancel(sender_id, cmd, **ext):
    send_options(sender_id, default=True)

@ampalibe.command(commands["get note"])
@mainview.render
def get_archive(sender_id, cmd, **ext):
    # leave search logic, now we have to use key-submit logic
        # todo: send options "parcourir" ou "rechercher"
        # chat.send_text(sender_id,  get_sentence("INPUT_KEYSEARCH"))
        # query.set_action(sender_id, actions["research"])
    actionview.prompt_note(sender_id)

@ampalibe.command(commands['render note'])
@mainview.render
def render_note(sender_id, cmd, note_id, **ext):
    mainview.render_note(sender_id, note_id)

# oriented mutation (<-)
@ampalibe.command(commands['create note'])
@mainview.render
def create_note(sender_id, cmd, **ext):
    for instruction in get_sentence("CREATE_NOTE_INSCRUCTIONS"):
        chat.send_text(sender_id, instruction)
    chat.send_text(sender_id, f"A la fin de la note, vous entrer le mot << {end_records_indicator} >>")
    send_options(sender_id, options=["confirm create note", "cancel"])
    query.set_action(sender_id, actions["create note"])

@ampalibe.command(commands["generate own key"])
@mainview.render
def generate_own_key(sender_id, cmd, **ext):
    actionview.prompt_key(sender_id)

@ampalibe.command(commands["render secure note"])
@mainview.render
def render_secure_note(sender_id, cmd, note_id, **ext):
    chat.send_text(sender_id, 'Entrer la clé de cette note: ')
    query.set_action(sender_id, actions["prompt note"])

@ampalibe.command(commands["update key"])
@mainview.render
def update_key(sender_id, cmd, **ext):
    new_key = query.get_temp(sender_id, "new_key")
    secret = query.get_temp(sender_id, 'secret')
    token = query.get_temp(sender_id, 'token')
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        note_id = payload["note_id"]
        note_instance_model.update_key(note_id, new_key)

        #todo: del token and secret and new_key temp variables used to update key
        for var_temp in ["secret", "token", "new_key"]:
            query.del_temp(sender_id, var_temp)
        
        chat.send_text(sender_id, "Clé mis à jour!")
        send_options(sender_id, default=True)
    except jwt.ExpiredSignatureError:
        chat.send_text(sender_id, "Délais d'attente un peu long, veuillez réessayer")
        send_options(sender_id, options=["edit key", "cancel"])
     

@ampalibe.command(commands["reedit key"])
@mainview.render
def edit_key(sender_id, cmd, note_id, **ext):
    secret = fake.dga()
    parse_note_id = ObjectId(note_id)

    token = jwt.encode(
        {"note_id": str(parse_note_id), "exp": datetime.now() + timedelta(minutes=2)},
        secret
    )
    query.set_temp(sender_id, 'secret', secret)
    query.set_temp(sender_id, 'token', token)
    chat.send_text(sender_id, "Entrer la nouvelle clé: ")
    query.set_action(sender_id, actions["prompt new key"])

@ampalibe.command(commands["edit key"])
@mainview.render
def edit_key(sender_id, cmd, note_id, **ext):
    secret = fake.dga()
    print(note_id)
    parse_note_id = ObjectId(note_id)
    token = jwt.encode(
        {"note_id": str(parse_note_id), "exp": datetime.now() + timedelta(minutes=2)},
        secret
    )
    query.set_temp(sender_id, 'secret', secret)
    query.set_temp(sender_id, 'token', token)
    chat.send_text(sender_id, 'Entrer la clé de cette note: ')
    query.set_action(sender_id, actions["edit key"])