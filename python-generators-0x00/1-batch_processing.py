#!/usr/bin/python3

from mysql.connector import Error

seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """
    Generator to fetch and process data in batches from the users database
    """
    try:
        connection = seed.connect_to_prodev()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:
                batch.append(row)
                if len(batch) == batch_size:  # When batch is full, yield it
                    yield batch
                    batch = []  # Reset batch

            if batch:  # Yield remaining rows if any
                yield batch

        else:
            raise ValueError("Failed to connect to ALX_prodev database.")
    
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        processed_batch = [user for user in batch if user['age'] > 25]
        
        for user in processed_batch:
            print(user)
