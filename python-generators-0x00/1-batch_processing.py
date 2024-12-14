#!/usr/bin/python3

from mysql.connector import Error

seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """
    Generator to fetch and process data in batches from the users database
    """
    try:
        with seed.connect_to_prodev() as connection:
            if connection and connection.is_connected():
                with connection.cursor(dictionary=True, buffered=True) as cursor:
                    query = ("SELECT user_id, name, email, age FROM user_data WHERE age >= %s LIMIT %s;")
                    cursor.execute(query, (25, batch_size))
                    for (user_id, name, email, age) in cursor:
                        yield { f"user_id: {user_id}, name: {name}, email: {email}, age: {age}" }
            else:
                raise ValueError("Failed to connect to ALX_prodev database.")
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    processes each batch to filter users over the age of25
    """
    for user in stream_users_in_batches(50):
        print(user)
        next(stream_users_in_batches(50))