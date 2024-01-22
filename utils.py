from os import environ as env
from models.archive import  get_all_archives

def is_user(keyword): 
    keypass = env.get('KEYPASS')
    return keyword == keypass


def load_search_data():
    all_archives = get_all_archives()
    DATA_SEARCH =  [archive['title'] for archive in all_archives]
    RECORD_SEARCH = [archive['records'] for archive in all_archives]
    return list(set(DATA_SEARC) | set(RECORD_SEARCH))