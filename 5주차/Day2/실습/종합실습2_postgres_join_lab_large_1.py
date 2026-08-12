import argparse
import getpass

import psycopg
from psycopg import sql

from config import connect


def create_role():
    password = getpass.getpass("skala_user 비밀번호: ")
    with connect() as connection:
        connection.execute(
            """
            DO $$
            BEGIN
              IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'skala_user') THEN
                CREATE ROLE skala_user LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
              END IF;
            END $$
            """
        )
        connection.execute(
            sql.SQL("ALTER ROLE skala_user PASSWORD {}").format(sql.Literal(password))
        )
    print("role 완료: skala_user")


def create_database():
    with psycopg.connect("postgresql:///postgres", autocommit=True) as connection:
        exists = connection.execute(
            "SELECT 1 FROM pg_database WHERE datname = 'skala_db'"
        ).fetchone()
        if not exists:
            connection.execute(
                "CREATE DATABASE skala_db OWNER skala_user ENCODING 'UTF8' TEMPLATE template0"
            )
    print("database 완료: skala_db")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "step", nargs="?", default="all", choices=("role", "database", "all")
    )
    step = parser.parse_args().step
    if step in ("role", "all"):
        create_role()
    if step in ("database", "all"):
        create_database()
