#!/usr/bin/python3

from mysql.connector import Error

seed = __import__('seed')

def stream_users():
    """
    A generator function that yields user data from the user_data table in the ALX_prodev database.
    """ 
    try:
        with seed.connect_to_prodev() as connection:
            if connection and connection.is_connected():
                with connection.cursor(dictionary=True, buffered=True) as cursor:
                        cursor.execute("SELECT user_id, name, email, age FROM user_data;")                        
                        for (user_id, name, email, age) in cursor:
                            yield { f"user_id: {user_id}, name: {name}, email: {email}, age: {age}" }                   
                        
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