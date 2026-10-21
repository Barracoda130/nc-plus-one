
import argparse

def seed_database():
    from src.db.seed import seed_database
    seed_database()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="NC Plus One",
        description="A command-line tool to manage the NC Plus One database.",
    )
    parser.add_argument("--seed", action="store_true", help="Seed the database")
    args = parser.parse_args()

    if args.seed:
        seed_database()
        print("Database seeded successfully.")
    else:
        print("No action specified. Nothing was done.")