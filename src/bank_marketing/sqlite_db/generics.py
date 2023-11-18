"""This module includes the functions to create connection object to sqlite database,
create data tables and remove them in/from sqlite database.
"""
import os
import sqlite3
from sqlite3 import Connection, Error


def create_connection(db_file: os.PathLike) -> Connection:
    """Create a database connection to the SQLite database specified by `db_file`

    Args:
    ----
        db_file(os.PathLike): File containing the database
    Returns:
        Connection to database
    """
    return sqlite3.connect(db_file, check_same_thread=False)


def create_table(conn: Connection, create_table_sql: str) -> None:
    """Create a table from the create_table_sql statement

    Args:
    ----
        conn (Connection): connection to database
        create_table_sql (str): SQL statement for table creation
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def remove_table(conn: Connection, table_name: str) -> None:
    """Delete then drop table from sql database

    Args:
    ----
        conn (Connection): connection to database
        table_name (str): Name of the table
    """
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name};")  # noqa
    cur.execute(f"DROP TABLE {table_name};")
    conn.commit()
