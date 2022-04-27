# this will contain all the logics for connecting, retreiving info or for all the functions 
# related with the database
from werkzeug.security import generate_password_hash
from psutil import users
from user import User
from pymongo import MongoClient
client=MongoClient('mongodb+srv://test:test@chatapp.mzhtn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

chat_db=client.get_database('ChatDB')
users_collection=chat_db.get_collection('users')

def save_users(username, email, password):
    password_hash=generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})
    # we are not gonna save passwords as mere statements so if someone gets our db he'll know all passwords
    # so we'll store them as HashPasswords

# save_users('ala','lo@k.com','shit')

def get_user(username):
    user_data=users_collection.find_one({'_id':username})
    # now directly return object of the class User inside user.py
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None