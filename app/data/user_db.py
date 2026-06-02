# Base de datos simulada en memoria
fake_db = [
    {
        "id": 1,
        "name": "Simon",
        "email": "simon@gmail.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Maria",
        "email": "maria@gmail.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Carlos",
        "email": "carlos@gmail.com",
        "role": "user",
        "is_active": True
    },
    {
        "id": 4,
        "name": "Ana",
        "email": "ana@gmail.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 5,
        "name": "Roberto",
        "email": "roberto@gmail.com",
        "role": "user",
        "is_active": False
    }
]
current_id = 6

def get_next_id():
    global current_id
    next_id = current_id
    current_id += 1
    return next_id

def reset_db():
    global fake_db, current_id
    fake_db = []
    current_id = 1