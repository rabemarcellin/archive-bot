from ampalibe import Payload
from ampalibe.ui import Element, Button, Type

def search_result_views(sender_id, chat, archives):
    list_items = []
    
    for archive in archives:
        buttons = [
            Button(
                type=Type.postback,
                title="voir",
                payload=Payload(f"/archive {archive['_id']}", id_item=archive['_id']),
            )
        ]

        list_items.append(
            Element(
                title=f"""{archive['title']}
                groupe: {archive['group_source']}
                """,
                buttons=buttons,
            )
        )

    chat.send_generic_template(sender_id, list_items, next=True)