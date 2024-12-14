#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, db, age=25, query):
        """
        constructor for the Database class

        Args:
            db: database name
            age: user age
        """
        self.db = db
        self.age = age
        self.conn = None
        self.query = query

    def __enter__(self):
        """
        Create connection with sqlit3 database to
        execute the query that was provided.

        return: cursor
        """
        try:
            self.conn = sqlite3.connect(self.db)
            self.cursor.execute(self.query, (self.parameter))
            return self.cursor
        except sqlite3.Error as error:
            print("Error:", error)
    
    def __exit__(self):
        """
        close connection to sqlit3 database
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()

with ExecuteQuery("SELECT * FROM usersm WHERE id < ? ", (5,)) as cursor:
    for row in cursor:
        print(row)