from .connection import db


def run_migrations():
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    """)
    print("Migrations applied successfully.")


if __name__ == "__main__":
    run_migrations()

