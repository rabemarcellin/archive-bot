from os import environ as env

def is_user(keyword): 
    keypass = env.get('KEYPASS')
    return keyword == keypass
