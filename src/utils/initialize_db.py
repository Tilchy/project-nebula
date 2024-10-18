import sqlite3
import logging
import os

from dotenv import load_dotenv

from ..users.register import UserRegister
from ..schemas.user import UserDto

logging.basicConfig(level=logging.INFO)

def init_sqlite_db(db_path: str) -> None:
    """
    Initialize an SQLite database with the given schema(s).

    Args:
        db_path (str): Path to the SQLite database file.

    Raises:
        sqlite3.Error: If there's an issue with the database connection or table creation.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query_create_users = f"""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            );
            """

            query_create_roles = f"""
            CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
            );
            """

            query_create_user_roles = f"""
            CREATE TABLE IF NOT EXISTS user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (user_uuid) REFERENCES users(uuid),
            FOREIGN KEY (role_id) REFERENCES roles(id)
            );
            """

            cursor.execute(query_create_users)
            cursor.execute(query_create_roles)
            cursor.execute(query_create_user_roles)

            conn.commit()
            logging.info("Database initialized successfully")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while initializing the database: {e}")
        raise

def insert_mock_data(db_path: str) -> None:
    """
    Insert mock data into the database.
    """
    user_admin = UserDto(name="admin", email="admin@test.com", password="password123")
    user1 = UserDto(name="tilen", email="tilen@test.com", password="password123")
    user2 = UserDto(name="jana", email="jana@test.com", password="password123")
    user3 = UserDto(name="ziga", email="ziga@test.com", password="password123")
    user4 = UserDto(name="jan", email="jan@test.com", password="password123")
    user_register = UserRegister()

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO roles (name) VALUES (?)", ("admin",))
            cursor.execute("INSERT INTO roles (name) VALUES (?)", ("user",))

            conn.commit()
            logging.info("Mock data inserted successfully")
    except sqlite3.Error as e: 
        logging.error(f"An error occurred while inserting mock data: {e}")
        raise

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            user_register.create_user(user1)
            user_register.create_user(user2)
            user_register.create_user(user3)
            user_register.create_user(user4)    
            user_register.create_user(user_admin)

            # Get the role IDs for "admin" and "user"
            cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
            admin_role_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT id FROM roles WHERE name = 'user'")
            user_role_id = cursor.fetchone()[0]

            cursor.execute("SELECT uuid FROM users WHERE name = ?", (user_admin.name,))
            user_admin_uuid = cursor.fetchone()[0]
            cursor.execute("INSERT INTO user_roles (user_uuid, role_id) VALUES (?, ?)", (user_admin_uuid, admin_role_id))

            for user in [user1, user2, user3, user4]:
                cursor.execute("SELECT uuid FROM users WHERE name = ?", (user.name,))
                user_uuid = cursor.fetchone()[0]
                cursor.execute("INSERT INTO user_roles (user_uuid, role_id) VALUES (?, ?)", (user_uuid, user_role_id))
      
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting mock data: {e}")
        raise


def remove_db_if_exists(db_path: str) -> None:
    """
    Remove the database file if it exists.
    """
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            logging.info(f"Removed existing database file: {db_path}")
        except OSError as e:
            logging.error(f"Error removing database file: {e}")
            raise
    else:
        logging.info(f"Database file does not exist: {db_path}")


# Example usage
if __name__ == "__main__":
    load_dotenv()
    db_path = os.getenv('DB_NAME')
    remove_db_if_exists(db_path)
    init_sqlite_db(db_path)
    insert_mock_data(db_path)
