import mysql.connector 
from dotenv import load_dotenv
import os

def connect_db(database=None):
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

        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database,
            'raise_on_warnings': True
        }

        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            return connection

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
    else:
        connection.close()
        return None
