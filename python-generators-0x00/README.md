# 📚 **SQL Row Streaming Generator**

## 🎯 **Objective 1**

Create a generator that streams rows from an SQL database one by one.

---

## 📋 **Instructions**

1. **Write a Python script** named `seed.py` to perform the following tasks:

2. **Set up the MySQL database**:

   - **Database Name**: `ALX_prodev`
   - **Table Name**: `user_data`
   - **Table Schema**:
     | **Column** | **Data Type** | **Constraints** |
     |-------------|-----------------|----------------------------|
     | `user_id` | `UUID` | **Primary Key**, **Indexed** |
     | `name` | `VARCHAR` | **NOT NULL** |
     | `email` | `VARCHAR` | **NOT NULL** |
     | `age` | `DECIMAL` | **NOT NULL** |

3. **Populate the database**:
   - Insert sample data from the `user_data.csv` file into the `user_data` table.

---

## ⚙️ **Function Prototypes**

| **Function**                        | **Description**                                               |
| ----------------------------------- | ------------------------------------------------------------- |
| `def connect_db()`                  | Connects to the MySQL database server.                        |
| `def create_database(connection)`   | Creates the `ALX_prodev` database if it does not exist.       |
| `def connect_to_prodev()`           | Connects to the `ALX_prodev` MySQL database.                  |
| `def create_table(connection)`      | Creates the `user_data` table if it does not exist.           |
| `def insert_data(connection, data)` | Inserts data into the `user_data` table if it does not exist. |

---

## 🎯 **Objective 2**

Create a generator that streams rows from an SQL database one by one.

---

## 📋 **Instructions**

1. **File Name**: `0-stream_users.py`

2. **Create a function** that streams rows from the `user_data` table using a **Python yield generator**.

3. **Function Prototype**:
   ```python
   def stream_users():
       """Streams rows from the 'user_data' table one by one using a generator."""
   ```
4. **Function Constraints**:

- The function should use only one loop to iterate through the result set.
- Each row should be streamed one-by-one from the user_data table.

---
