

from src.db.connection import get_connection
from src.db.drop_tables import drop_all_tables

def test_drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables first
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY);")
    cursor.execute("CREATE TABLE IF NOT EXISTS venues (id SERIAL PRIMARY KEY);")
    cursor.execute("CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY);")
    cursor.execute("CREATE TABLE IF NOT EXISTS rsvps (id SERIAL PRIMARY KEY);")
    
    conn.commit()

    # Now drop all tables
    drop_all_tables()

    # Check if tables are dropped
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [table[0] for table in cursor.fetchall()]

    assert "users" not in tables
    assert "venues" not in tables
    assert "events" not in tables
    assert "rsvps" not in tables

    cursor.close()
    conn.close()
    
def test_drop_all_tables_when_no_tables_exist():
    drop_all_tables()  # Attempt to drop tables when none exist
    drop_all_tables()  # Attempt to drop tables again to ensure no errors occur
    
    
    