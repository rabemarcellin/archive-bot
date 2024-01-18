import ampalibe
from ampalibe import Model, Messenger
from os import environ as env
from utils import is_user
from views.action import get_main_options, is_continue, upload_archive_data
from views.template import search_result_views
from models.archive import create_db_archive, get_all_archives, get_title_archive, get_db_archive
import rapidfuzz

GET_PASSWORD_INPUT = env.get('GET_PASSWORD_INPUT')
GET_SEARCHKEY_INPUT = env.get('GET_SEARCHKEY_INPUT')
LOGOUT_WISH_TEXT = env.get('LOGOUT_WISH_TEXT')
CREATE_ARCHIVE_INSCRUCTIONS = env.get('CREATE_ARCHIVE_INSCRUCTIONS')
GET_TITLE_INPUT = env.get('GET_TITLE_INPUT')
BAD_CREDENTIALS_TEXT = env.get('BAD_CREDENTIALS_TEXT')
SEARCH_NOT_FOUND = env.get('SEARCH_NOT_FOUND')
END_UPLOAD = env.get('END_UPLOAD')

ALL_ARCHIVES = get_all_archives()
DATA_SEARCH = [archive['title'] for archive in ALL_ARCHIVES]
RECORD_SEARCH = [archive['records'] for archive in ALL_ARCHIVES]

chat = Messenger()
query = Model()

chat.get_started()

is_logged = False

@ampalibe.command('/')
def main(sender_id, cmd, **ext):
    global is_logged
    if not is_logged:
        chat.send_text(sender_id, GET_PASSWORD_INPUT)
        query.set_action(sender_id, '/login')
    else:
        get_main_options(sender_id, chat)

    
@ampalibe.command('/get_archive')
def get_archive(sender_id, cmd, **ext):
    chat.send_text(sender_id, GET_SEARCHKEY_INPUT)
    query.set_action(sender_id, '/keysearch')

@ampalibe.command('/logout')
def logout(sender_id, cmd, **ext):
    global is_logged
    is_logged = False
    chat.send_text(sender_id, LOGOUT_WISH_TEXT)

@ampalibe.command('/archive')
def archive(sender_id, cmd, id_item, **ext):
    archive = get_db_archive(id_item)
    chat.send_text(sender_id,
    f"""*{archive['title']}*

    {archive['records']}
    """
    )
    is_continue(sender_id, chat, "")

@ampalibe.command('/create_archive')
def create_archive(sender_id, cmd, **ext):
    query.set_temp(sender_id, 'is_finish', False)
    query.set_temp(sender_id, 'title', None)
    query.set_temp(sender_id, 'group_source', None)
    query.set_temp(sender_id, 'records', None)
    chat.send_text(sender_id, CREATE_ARCHIVE_INSCRUCTIONS) 
    is_continue(sender_id, chat, "upload_archive")
    
@ampalibe.command('/upload_archive')
def upload_archive(sender_id, cmd, **ext):
    title = query.get_temp(sender_id, 'title')
    if not title:
        chat.send_text(sender_id, GET_TITLE_INPUT)
        return query.set_action(sender_id, '/upload_archive')

@ampalibe.action('/login')
def login(sender_id, cmd, **ext):
    if not is_user(cmd):
        chat.send_text(sender_id, BAD_CREDENTIALS_TEXT)
        is_continue(sender_id, chat, "")
    else:
        global is_logged
        is_logged = True
        get_main_options(sender_id, chat)

@ampalibe.action('/is_record_finish')
def is_record_finish(sender_id, cmd, **ext):
    title = query.get_temp(sender_id, 'title')
    group_source = query.get_temp(sender_id, 'group_source')
    records = query.get_temp(sender_id, 'records')

    if cmd == END_UPLOAD:
        chat.send_text(sender_id, f"{records}")
        create_db_archive(title, group_source, records)
        is_continue(sender_id, chat, "")
    else:
        query.set_temp(sender_id, 'records', f"{records}\n\n{cmd}" if records else cmd)
        chat.send_text(sender_id, f'alefaso ny manaraka na soraty ny hoe "{END_UPLOAD}"')
        query.set_action(sender_id, '/is_record_finish')

@ampalibe.action('/upload_archive')
def upload_archive(sender_id, cmd, **ext):
    upload_archive_data(sender_id, chat, query, cmd)

@ampalibe.action('/keysearch')
def use_keysearch(sender_id, cmd, **ext):
    keysearch = cmd
    search_results = rapidfuzz.process.extract(keysearch, list(set(DATA_SEARCH) | set(RECORD_SEARCH)))
    archive_search_results = [
        get_title_archive(title) 
        for (title, match_in_percent, index) 
        in search_results 
        if match_in_percent > 80
    ]
    if len(archive_search_results) == 0:
        chat.send_text(sender_id, SEARCH_NOT_FOUND)
        is_continue(sender_id, chat, "")
    else:
        search_result_views(sender_id=sender_id, chat=chat, archives=archive_search_results)
        is_continue(sender_id, chat, "")




    

   

        

    
    


  
