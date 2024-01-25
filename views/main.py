import re
from ampalibe.messenger import Filetype
from ampalibe.ui import Button
from globalinstance import note_model, chat
from .action import send_options


def render(func):
    def call_render(*args, **kwargs):
        sender_id = kwargs['sender_id']
        chat.send_action(sender_id, 'mark_seen')
        chat.send_action(sender_id, 'typing_on')
        func(*args, **kwargs)
        chat.send_action(sender_id, 'typing_off')
    return call_render


def render_note(sender_id, note_id):
    note = note_model.get_by_id(note_id)
    chat.send_text(sender_id, note['title'])
    pattern = re.compile(r'^https://scontent\.xx\.fbcdn\.net/')

    for one_message in note['records']:
        if pattern.match(one_message):
            print(one_message)
            chat.send_file_url(sender_id, one_message, filetype=Filetype.image)
        else:
            chat.send_text(sender_id, one_message)
    send_options(sender_id, options=["get note", "go main menu"])

