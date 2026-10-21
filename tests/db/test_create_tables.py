

from src.db.connection import get_connection
from src.db.create_tables import create_all_tables
from src.db.drop_tables import drop_all_tables


def test_create_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    drop_all_tables() 
    
    conn.commit()

    create_all_tables()
    

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [table[0] for table in cursor.fetchall()]

    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables

    cursor.close()
    conn.close()
    
def test_create_all_tables_already_exist():
    create_all_tables()  # Create tables for the first time
    create_all_tables()  # Attempt to create tables again
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [table[0] for table in cursor.fetchall()]
    
    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables
    
    cursor.close()
    conn.close()
    