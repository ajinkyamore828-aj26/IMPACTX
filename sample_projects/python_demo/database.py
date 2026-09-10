
import utils

def connect_db(connection_string):
    utils.logger_helper(f"Connecting to {connection_string}")
    return {"status": "connected", "dsn": connection_string}

def query_user(email):
    return {"username": "admin", "email": email, "hash": "hashed_secret123"}

def insert_record(table, data):
    utils.logger_helper(f"Inserted record into {table}")
    return True
