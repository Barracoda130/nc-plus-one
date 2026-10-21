

from src.db.connection import get_connection
from src.db.create_tables import create_all_tables
from src.db.seed import seed_database, seed_users



def test_seed_database_creates_tables_and_seeds_users():
    seed_database()
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [table[0] for table in cursor.fetchall()]

    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables

    cursor.execute("SELECT COUNT(*) FROM users;")
    user_count = cursor.fetchone()[0]
    
    assert user_count > 0
    
def test_seed_database_produces_identical_state():
    seed_database()
    
    conn1 = get_connection()
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM users, venues, events, rsvps;")
    database_data1 = cursor1.fetchall()
    cursor1.close()
    conn1.close()
    
    seed_database()
    
    conn2 = get_connection()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM users, venues, events, rsvps;")
    database_data2 = cursor2.fetchall()

    cursor2.close()
    conn2.close()
    
    assert database_data1 == database_data2
    
    
    