
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(".env")

def get_connection():
    database_name = os.environ.get("DATABASE_NAME")
    database_user = os.environ.get("DATABASE_USER")
    database_password = os.environ.get("DATABASE_PASSWORD")
    print(f"Connecting to database: {database_name} with user: {database_user}")
    print(f"Using password: {database_password}")
    
    connection = psycopg2.connect(
        dbname=database_name,
        user=database_user,
        password=database_password,
        host="localhost"
    )
    return connection

    