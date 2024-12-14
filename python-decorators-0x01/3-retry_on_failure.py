import time
import sqlite3 
import functools

#### paste your with_db_decorator here

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("user.db")
            return func(conn, *args, **kwargs)
        except sqlite3.Error as error:
            print("Error:", error)
        finally:
            if conn:
                conn.close()
            
    return wrapper_with_db_connection

def retry_on_failure(retries=3, delay=1):
    def decorator_retry_on_failure(func):
        @functools.wraps(func)
        def wrapper_retry_on_failure(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                     return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts < retries:
                        time.sleep(delay)
                        print(f"attempt {attempts} / {retries} failed: {e} ")
                    else:
                        print("All attempts failed")
                        raise
        return wrapper_retry_on_failure
    return decorator_retry_on_failure

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)