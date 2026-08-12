# /// script
# dependencies = ["psycopg[binary]"]
# ///

import os

import psycopg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql:///skala_db",
)


def connect():
    return psycopg.connect(DATABASE_URL)


if __name__ == "__main__":
    with connect() as connection:
        database, user = connection.execute(
            "SELECT current_database(), current_user"
        ).fetchone()
        print(f"PostgreSQL 연결 성공: database={database}, user={user}")
