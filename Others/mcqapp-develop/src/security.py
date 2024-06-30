import json

from src.utils.db_class import DbUtils

db_operations = DbUtils()


def register(content):
    try:
        db_operations.db['users'].insert_one(content)
        return "Successfully Created User Profile"
    except:
        return "Sorry! User Profile Could not be craeted.Try Again"


def login(content):
    try:
        data = db_operations.db['users'].find_one({'email': content['email'], 'password': content['password']})
        print(data)
        if (data):
            if (data['password'] == content['password']):
                print({'state': '1', 'username': data['username']})
                return json.dumps({'state': '1', 'username': data['username']})
            else:
                return '0'
        else:
            return '0'
    except:
        return '0'