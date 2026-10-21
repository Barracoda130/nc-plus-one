
import argparse
import asyncio

def run_seed_database():
    from src.db.setup.seed import seed_database
    asyncio.run(seed_database())
    
def run_debug_pytest():
    import pytest
    pytest.main(["-s", "tests/db/test_create_tables.py", "--disable-warnings"])

def run_app():
    from src.app import run
    run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="NC Plus One",
        description="A command-line tool to manage the NC Plus One database.",
    )

    parser.add_argument("--debug-tests", action="store_true", help="Run pytest in debug mode")
    parser.add_argument("--seed", action="store_true", help="Seed the database")
    parser.add_argument("--run", action="store_true", help="Run the application. This is also the behaviour if no args are passed")

    args = parser.parse_args()

    if args.seed:
        run_seed_database()
        print("Database seeded successfully.")
    elif args.debug_tests:
        run_debug_pytest()
    else:
        run_app()