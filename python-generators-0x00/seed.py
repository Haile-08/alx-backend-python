import mysql.connector 
from dotenv import load_dotenv
import os

def connect_db():
    """
    Connects to the mysql database server

    Returns:
        connection: A MySQL connection object if successful, otherwise None.
    """
    load_dotenv()

    try:
        host = os.getenv("DATABASE_HOST_NAME")
        user = os.getenv("DATABASE_USER_NAME")
        password = os.getenv("DATABASE_USER_PASSWORD")

        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
        )

        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Python database connection error: {e}")
        return None