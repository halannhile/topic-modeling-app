from .operations import DatabaseOperations

def init_db(db_uri):
    db_operations = DatabaseOperations(db_uri)
    return db_operations
