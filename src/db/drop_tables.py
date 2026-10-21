

from src.db.connection import get_connection

TABLE_NAMES = ["rsvps", "events", "venues", "users"]

def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    for table_name in TABLE_NAMES:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
    conn.commit()
    cursor.close()
    conn.close()