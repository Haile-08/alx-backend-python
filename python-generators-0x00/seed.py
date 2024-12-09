#!/usr/bin/python3

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


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    
    Args:
        connection: A MySQL connection object.
    
    Returns:
        nothing
    """
    try:
        if connection and connection.is_connected():
             with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")

        else:
            raise ValueError("Error database not connected.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def connect_to_prodev():
    """
    Connects the the ALX_prodev database in MYSQL

    Returns:
        connection: A MySQL connection object if successful, otherwise None.
    """
    try:
        connection = connect_db(database="ALX_prodev")

        if connection and connection.is_connected():
            return connection

        else:
            raise ValueError("Can not connect to ALX_prodev database.")

    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exists with the required fields

    Args:
        connection: A MySQL connection object.
    
    Returns:
        nothing
    """
    try:
        if connection and connection.is_connected():
             with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL(3, 0) NOT NULL
                )
            """)
            connection.commit()

        else:
            raise ValueError("Error database not connected.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def insert_data(connection, data):
    """
    Inserts data in the database if it does not exist

    Args:
        connection: A MySQL connection object.
        data: The path to the CSV file containing the data to be inserted.

    Returns:
        None
    """
    try:
        if not connection or not connection.is_connected():
            raise ValueError("Database not connected or connection not available.")

        with connection.cursor() as cursor:
            cursor.execute("USE ALX_prodev;")

            with open(data, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                insert_query = """
                    INSERT INTO user_data (name, email, age) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    age = VALUES(age);
                """

                required_headers = {"name", "email", "age"}
                rows_to_insert = []
                if not required_headers.issubset(reader.fieldnames):
                    raise ValueError(f"CSV file is missing required headers: {required_headers - set(reader.fieldnames)}")

                for row in reader:
                    name = row["name"].strip()
                    email = row["email"].strip()
                    try:
                        age = int(row["age"])
                    except ValueError:
                        logging.warning(f"Skipping row with invalid age: {row}")
                        continue

                    rows_to_insert.append((name, email, age))

                if rows_to_insert:
                    cursor.executemany(insert_query, rows_to_insert)
                    connection.commit()
                else:
                    print("No valid rows to insert.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {data}")
        logging.error(f"File not found: {e}")ush

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"Value error: {e}")

    except Error as e:
        print(f"Database error: {e}")
        logging.error(f"Database error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")