from ampalibe import Payload
from ampalibe.ui import QuickReply, Button
from globalinstance import fake
from utils import build_command, get_sentence

end_records_indicator = get_sentence("end records indicator")

commands = {
    "root": build_command(""),
    "get note": build_command("get_note"),
    "render note": build_command("render_note"),
    "research": build_command("research"),
    "cancel": build_command("cancel"),
    "create note": build_command("create_note"),
    "confirm create note": build_command("confirm_create_note"),
    "generate own key": build_command("generate_own_key"),
    "generate random key": build_command("generate_random_key"),
    "create another note": build_command("create_another_note"),
    "register note": build_command("register note"),
    "end records": build_command("end_records"),
    "libraries": build_command("libraries"),
    "edit key": build_command("edit_key"),
    "update key": build_command("update_key"),
    "reedit key": build_command("reedit_key"),
    "render secure note": build_command("render_secure_note")
}

actions = {
    "research": build_command("research"),
    "create note": build_command("create_note"),
    "prompt note": build_command("prompt_note"),
    "prompt title": build_command("prompt_title"),
    "prompt source ref": build_command("prompt_source_ref"),
    "prompt records": build_command("prompt_records"),
    "prompt key": build_command("prompt_key"),
    "generate key": build_command("generate_key"),
    "register note": build_command("register_note"),
    "edit key": build_command("edit key"),
    "prompt new key": build_command("prompt new key")
}

persistent_menu = [
    Button(type='postback', title=get_sentence("libraries"), payload=Payload(commands["libraries"])),
    Button(type='postback', title=get_sentence("get note"), payload=Payload(commands["get note"])),
    Button(type='postback', title=get_sentence("create note"), payload=Payload(commands["create note"]))
]

exist_options = {
    "go main menu": QuickReply(
        title=get_sentence("go main menu"),
        payload=Payload(commands["root"]),
        name="go to the main menu",
        ref=f"{fake.ean(length=13)}"
    ),
    "get note": QuickReply(
        title=get_sentence("get note"),
        payload=Payload(commands["get note"]),
        name="get a note",
        ref=f"{fake.ean(length=13)}"
    ),
    "create note": QuickReply(
        title=get_sentence("create note"),
        payload=Payload(commands["create note"]),
        name="create a note",
        ref=f"{fake.ean(length=13)}"
    ),
    "create another note": QuickReply(
        title=get_sentence("create another note"),
        payload=Payload(commands["create another note"]),
        name="create another note",
        ref=f"{fake.ean(length=13)}"
    ),
    "confirm create note": QuickReply(
        title=get_sentence("confirm create note"),
        payload=Payload(commands["confirm create note"]),
        name="confirm create note",
        ref=f"{fake.ean(length=13)}"
    ),
    "register note": QuickReply(
        title=get_sentence("register note"),
        payload=Payload(commands["register note"]),
        name="register note",
        ref=f"{fake.ean(length=13)}"
    ),
     "research": QuickReply(
        title=get_sentence("research"),
        payload=Payload(commands["get note"]),
        name="research a note",
        ref=f"{fake.ean(length=13)}"
    ),
     "cancel": QuickReply(
        title=get_sentence("cancel"),
        payload=Payload(commands["cancel"]),
        name="cancel",
        ref=f"{fake.ean(length=13)}"
    ),
     "generate own key": QuickReply(
        title=get_sentence("own key"),
        payload=Payload(commands["generate own key"]),
        name="generate own key",
        ref=f"{fake.ean(length=13)}"
    ),
     "generate random key": QuickReply(
        title=get_sentence("random key"),
        payload=Payload(commands["generate random key"]),
        name="generate random key",
        ref=f"{fake.ean(length=13)}"
    ),
    "end records": QuickReply(
        title=get_sentence("end records"),
        payload=Payload(commands["end records"]),
        name="end records",
        ref=f"{fake.ean(length=13)}"
    ),
    "libraries": QuickReply(
        title=get_sentence("libraries"),
        payload=Payload(commands["libraries"]),
        name="end records",
        ref=f"{fake.ean(length=13)}"
    ),
     "update key": QuickReply(
        title=get_sentence("update key"),
        payload=Payload(commands["update key"]),
        name="end records",
        ref=f"{fake.ean(length=13)}"
    ),
    "reedit key": QuickReply(
        title=get_sentence("reedit key"),
        payload=Payload(commands["reedit key"]),
        name="end records",
        ref=f"{fake.ean(length=13)}"
    ),
    "edit key": QuickReply(
        title=get_sentence("reedit key"),
        payload=Payload(commands["edit key"]),
        name="end records",
        ref=f"{fake.ean(length=13)}"
    ),
}

