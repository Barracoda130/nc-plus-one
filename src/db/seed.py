

import json
from argon2 import PasswordHasher

from src.db.connection import get_connection
from src.db.create_tables import create_all_tables
from src.db.drop_tables import drop_all_tables




def seed_users():
    conn = get_connection()
    cursor = conn.cursor()
    
    ph = PasswordHasher()

    # Insert from db/data/users.json
    with open("db/data/users.json", "r") as file:
        users_data = json.load(file)
        for user in users_data:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);",
                (user["name"], user["email"], ph.hash(user["password"]))
            )
            
    conn.commit()
    cursor.close()
    conn.close()
    

def seed_database():
    drop_all_tables()
    create_all_tables()
    seed_users()