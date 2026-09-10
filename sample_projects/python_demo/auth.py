
import database
import utils

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def validate(self):
        return utils.sanitize_input(self.username) != ""

def login(email, password):
    user_record = database.query_user(email)
    if user_record and hash_password(password) == user_record.get("hash"):
        return User(user_record["username"], email)
    return None

def register(username, email, password):
    hashed = hash_password(password)
    return database.insert_record("users", {"username": username, "email": email, "hash": hashed})

def hash_password(password):
    return utils.logger_helper("hashing") or "hashed_" + password
