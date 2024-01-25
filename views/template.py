from ampalibe import Payload
from ampalibe.ui import Element, Button, Type
from globalinstance import chat
from datas import commands

def render_note_items(sender_id, notes):
    note_items = []
    for note in notes:
        buttons = [
            Button(
                type=Type.postback,
                title="voir",
                payload=Payload(commands["render note"], note_id=note.id),
            )
        ]

        note_items.append(
            Element(
                title=f"""{note.title}\n
                source: {note.source_ref}
                """,
                buttons=buttons,
            )
        )

    chat.send_generic_template(sender_id, note_items, next=True)