from os import environ
from flask import g, current_app
import mysql.connector.pooling
import contextlib

DB_CONFIG = {
    "pool_name": environ.get("APP_DB_POOL_NAME", "quotes_pool"),
    "user": environ.get("APP_DB_USER", "app_user"),
    "password": environ.get("APP_DB_PASSWORD", "1234"),
    "host": environ.get("APP_DB_HOST", "localhost"),
    "port": int(environ.get("APP_DB_PORT", "3306")),
    "database": environ.get("APP_DB_NAME", "quotes_db"),
}


def connection_context():
    return contextlib.closing(get_connection())


def get_pool():
    if "db_pool" not in g:
        g.db_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
    return g.db_pool


def get_connection():
    if "db_conn" not in g:
        g.db_conn = get_pool().get_connection()

    return g.db_conn


def close_connection(e=None):
    db_conn = g.pop("db_conn", None)
    if db_conn is not None:
        db_conn.close()


def init_db():
    """
    TODO
    """
    with connection_context() as connection:
        with current_app.open_resource("schema.sql") as f:
            connection.executescript(f.read().decode("utf8"))
