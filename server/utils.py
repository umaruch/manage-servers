"""
    Вспомогательные функции
"""
import sqlite3

# Создание всех таблиц в БД
def create_all(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE servers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE commands(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            args TEXT NOT NULL,

            FOREIGN KEY (server_id)
                REFERENCES servers(id)
        )
        """
    )
    conn.commit()