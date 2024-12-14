#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db):
        """
        constructor for Database class

        Args:
            db: database name
        """
        self.db = db
        self.conn = None

    def __enter__(self):
        """
        create connection to sqlit3 database

        Return: the database connection
        """
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self):
        """
        close connection to sqlit3 database
        """
        if self.conn:
            self.conn.close()

with DatabaseConnection("users.db") as connection:
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor:
            print(row)
    except Exception as e:
        print(e)