from ampalibe import Payload
from ampalibe.ui import Element, Button, Type
from globalinstance import chat
from utils import get_sentence
from datas import commands

def render_note_items(sender_id, notes):
    note_items = []
    for note in notes:
        buttons = [
            Button(
                type=Type.postback,
                title="voir",
                payload=Payload(commands["render secure note"], note_id=note._id),
            ),
            Button(
                type=Type.postback,
                title=get_sentence("edit key"),
                payload=Payload(commands["edit key"], note_id=note._id),
            ),
        ]

        note_items.append(
            Element(
                title=f"""{note.title}
                \nsource: {note.source_ref}
                """,
                buttons=buttons,
            )
        )

    chat.send_generic_template(sender_id, note_items, next='Page suivante')