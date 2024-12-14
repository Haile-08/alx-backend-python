import sqlite3 
import functools

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

def transactional(func):
    @functools.wraps(func)
    def wrapper_transactional(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as error:
            conn.rollback()

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')