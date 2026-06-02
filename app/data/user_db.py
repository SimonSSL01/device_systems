# Base de datos simulada en memoria
fake_db = []
current_id = 1

def get_next_id():
    global current_id
    next_id = current_id
    current_id += 1
    return next_id

def reset_db():
    global fake_db, current_id
    fake_db = []
    current_id = 1