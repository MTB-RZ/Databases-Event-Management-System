import os
import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "*****"),
    "database": os.getenv("DB_NAME", "event_management"),
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as error:
        raise RuntimeError(f"Database connection failed: {error}") from error


def fetch_all(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def fetch_one(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def execute_procedure(procedure_name, args=None, fetch=False):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.callproc(procedure_name, args or [])
        results = []
        if fetch:
            for result in cursor.stored_results():
                results.extend(result.fetchall())
        connection.commit()
        return results
    except Error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
