from ampalibe import Payload
from ampalibe.ui import QuickReply
from os import environ as env

GET_ARCHIVE_TEXT = env.get('GET_ARCHIVE_TEXT')
CREATE_ARCHIVE_TEXT = env.get('CREATE_ARCHIVE_TEXT')
MAIN_WAY_TEXT = env.get('MAIN_WAY_TEXT')
CONTINUE_TEXT = env.get('CONTINUE_TEXT')
GOBACK_TEXT = env.get('GOBACK_TEXT')
GOBACK_MAIN = env.get('GOBACK_MAIN')
LOGOUT_TEXT = env.get('LOGOUT_TEXT')
CONFIRM_TEXT = env.get('CONFIRM_TEXT')
GET_GROUP_INPUT = env.get('GET_GROUP_INPUT')
GET_RECORD_INPUT = env.get('GET_RECORD_INPUT')

def get_main_options(sender_id, chat):
    quick_rep = [
        QuickReply(
            title=GET_ARCHIVE_TEXT,
            payload=Payload('/get_archive', name='get_archive', ref='fsdacjfklqsjdm789779')
        ),
        QuickReply(
            title=CREATE_ARCHIVE_TEXT,
            payload=Payload('/create_archive', name='create_archive', ref='fdsjqk4654654fsdfs')
        )
    ]
    chat.send_quick_reply(sender_id, quick_rep, MAIN_WAY_TEXT)

def is_continue(sender_id, chat, command_name):
    quick_rep = [
        QuickReply(
            title=CONTINUE_TEXT if command_name != "" else GOBACK_MAIN,
            payload=Payload(f'/{command_name}', name= command_name, ref='fsdacfsdfdsqmj778er')
        ),
        QuickReply(
            title=GOBACK_TEXT,
            payload=Payload('/', name='main', ref='ffdsfsdf7897fds')
        ),
        QuickReply(
            title=LOGOUT_TEXT,
            payload=Payload('/logout', name='logout', ref='jljmlkj798d7fsf')
        )
    ]
    chat.send_quick_reply(sender_id, quick_rep, CONFIRM_TEXT)


def upload_archive_data(sender_id, chat, query, cmd):
    is_finish = query.get_temp(sender_id, 'is_finish')
    title = query.get_temp(sender_id, 'title')
    group_source = query.get_temp(sender_id, 'group_source')
    records = query.get_temp(sender_id, 'records')

    if not title:
        query.set_temp(sender_id, 'title', cmd)

    if not group_source:
        query.set_temp(sender_id, 'group_source', True)
        chat.send_text(sender_id, GET_GROUP_INPUT)
        return query.set_action(sender_id, '/upload_archive')

    if not is_finish and not records:
        query.set_temp(sender_id, 'group_source', cmd)
        chat.send_text(sender_id, GET_RECORD_INPUT)
        return query.set_action(sender_id, '/is_record_finish')    