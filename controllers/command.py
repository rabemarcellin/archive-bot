import ampalibe
from utils import get_sentence
from datas import commands, actions, persistent_menu, end_records_indicator
from globalinstance import chat, query, fake, note_instance_model
from views import main as mainview
import views.action as actionview
from views.action import send_options


chat.get_started()

# oriented render (->)
@ampalibe.command(commands["root"])
@mainview.render
def main(sender_id, cmd, **ext):
    chat.persistent_menu(sender_id, persistent_menu)
    send_options(
        sender_id, 
        header_text=get_sentence("ROOT_OPTIONS_HEADER"), 
        options=["get note", "create note"]
    )

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

@ampalibe.command(commands["generate random key"])
@mainview.render
def generate_random_key(sender_id, cmd, **ext):
    #todo : genarate faker random key
    random_key = fake.nic_handle()
    note_instance = note_instance_model.get_by_key(random_key)
    # todo: render note
    mainview.render_note(sender_id, note_instance.note_id)
    
@ampalibe.command(commands["create another note"])
@mainview.render
def create_another_note(sender_id, cmd, **ext):
    query.send_text("Entre n'importe quelle touche pour continuer")
    query.set_action(sender_id, actions["create note"])