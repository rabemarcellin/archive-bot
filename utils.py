import json
from os import environ as env, getcwd
from pathlib import Path

def build_command(cmd):
    return f"/{cmd}"

def is_user(keyword): 
    keypass = env.get('KEYPASS')
    return keyword == keypass

def get_env_value(env_key):
    return env.get(env_key)

def get_sentence(sentence_key):
    currentDir = getcwd()
    file_name = "sentence.json"
    with open(f"{Path(currentDir).joinpath(file_name)}", "r") as read_file:
        sentence_lib = json.load(read_file)
        return sentence_lib[sentence_key]


def load_search_data(note_model):
    all_archives = note_model.get_all()
    DATA_SEARCH =  [archive.title for archive in all_archives]
    RECORD_SEARCH = [archive.records for archive in all_archives]
    return DATA_SEARCH + RECORD_SEARCH
