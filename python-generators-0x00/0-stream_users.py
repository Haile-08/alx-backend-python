#!/usr/bin/python3

from mysql.connector import Error

seed = __import__('seed')

def stream_users():
    """
    A generator function that yields user data from the user_data table in the ALX_prodev database.
    """ 
    try:
        connection = seed.connect_to_prodev()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")                        
            for row in cursor:
                yield {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                }       
        else:
            raise ValueError("Failed to connect to ALX_prodev database.")
    
    except TypeError as e:
            print(f"Error connecting to ALX_prodev: {e}")
            return None

    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()

