

from src.db.connection import get_connection
import psycopg2

SCHEMA_FILE = "db/schema.sql"

def create_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r") as file:
        schema_sql = file.read()
        cursor.execute(schema_sql)
        
    conn.commit()
    cursor.close()
    conn.close()
    
    
def create_table(table_name: str, conn: psycopg2.extensions.connection):
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r") as file:
        schema_sql = file.read()
        create_table_sql = schema_sql.split(f"CREATE TABLE {table_name}")[1].split(";")[0]
        cursor.execute(f"CREATE TABLE {table_name}" + create_table_sql)
        
    conn.commit()
    cursor.close()


def create_users_table(conn: psycopg2.extensions.connection):
    create_table("users", conn)

def create_venues_table(conn: psycopg2.extensions.connection):
    create_table("venues", conn)

def create_events_table(conn: psycopg2.extensions.connection):
    create_table("events", conn)
    
def create_rsvps_table(conn: psycopg2.extensions.connection):
    create_table("rsvps", conn)