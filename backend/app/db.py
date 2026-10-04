import os

import psycopg


def get_connection():
    """Open a connection to PostgreSQL.

    All connection details come from environment variables, so no password
    or host is ever written into the code or committed to GitHub.
    """
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "resolvai"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=5,
    )