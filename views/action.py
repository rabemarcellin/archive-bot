from ampalibe import Payload
from ampalibe.ui import QuickReply
from utils import get_sentence
from globalinstance import chat, query
from datas import exist_options, actions


def send_options(sender_id, default=False, options=[],
                 header_text=get_sentence("default options header")):
    selected_options = []
    if default:
       selected_options.append(exist_options["go main menu"]) 
    else:
        for option in options:
            selected_options.append(exist_options[option])
    chat.send_quick_reply(sender_id, selected_options, header_text)

def generate_key_options(sender_id):
    chat.send_text(sender_id, get_sentence("create note successfully"))
    chat.send_text(sender_id, get_sentence("generate key instruction")) 
    send_options(
        sender_id, 
        header_text=get_sentence("generate key header"), 
        options=["generate own key", "generate random key"]
    )
    query.set_action(sender_id, actions["generate key"])

def prompt_note(sender_id):
    chat.send_text(sender_id, get_sentence("input key note"))
    query.set_action(sender_id, actions["prompt note"])

def prompt_key(sender_id):
    query.set_temp(sender_id, 'notekey', None)
    chat.send_text(sender_id, get_sentence("input key"))
    query.set_action(sender_id, actions["generate key"])

def prompt_title(sender_id, notequery):
    if notequery.title is None:
        chat.send_text(sender_id, get_sentence("INPUT_TITLE"))
        return query.set_action(sender_id, actions["prompt title"])

def prompt_source_ref(sender_id, notequery):
    if notequery.source_ref is None:
        chat.send_text(sender_id, get_sentence("INPUT_SOURCE_REFERENCE"))
        return query.set_action(sender_id, actions["prompt source ref"])

def prompt_records(sender_id, notequery):
    if len(notequery.records) == 0:
        chat.send_text(sender_id, get_sentence("INPUT_NOTE"))
    elif len(notequery.records) > 0:
        send_options(sender_id, header_text="**_**", options=["end records"])
    return query.set_action(sender_id, actions["prompt records"])
