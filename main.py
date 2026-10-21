
import argparse

def seed_database():
    from src.db.seed import seed_database
    seed_database()
    
def debug_pytest():
    import pytest
    pytest.main(["-s", "tests/db/test_create_tables.py", "--disable-warnings"])
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="NC Plus One",
        description="A command-line tool to manage the NC Plus One database.",
    )
    parser.add_argument("--debug-tests", action="store_true", help="Run pytest in debug mode")
    parser.add_argument("--seed", action="store_true", help="Seed the database")
    args = parser.parse_args()

    if args.seed:
        seed_database()
        print("Database seeded successfully.")
    elif args.debug_tests:
        debug_pytest()
    else:
        print("No action specified. Nothing was done.")