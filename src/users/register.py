import sqlite3
import os
import logging
import uuid

from dotenv import load_dotenv
from ..schemas.user import User, UserDto
from ..utils.password import PasswordHelper

logging.basicConfig(level=logging.INFO)

class UserRegister():
    def __init__(self):
        load_dotenv()
        self.db_path = os.getenv('DB_NAME')

    def create_user(self, user: UserDto) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM users WHERE name = ? OR email = ?"
                cursor.execute(query, (user.name, user.email))
                result = cursor.fetchone()

                if result:
                    logging.error(f"User with name {user.name} or email {user.email} already exists")
                    return {"message": f"User with name {user.name} or email {user.email} already exists"}

        except sqlite3.Error as e:
            logging.error(f"Error checking if user exists: {e}")
            return {"message": f"Error checking if user exists: {e}"}

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                INSERT INTO users (uuid, name, email, password)
                VALUES (?, ?, ?, ?)
                '''

                query_add_role = "INSERT INTO user_roles (user_uuid, role_id) VALUES (?, ?)"

                cursor.execute("SELECT id FROM roles WHERE name = 'user'")
                user_role_id = cursor.fetchone()[0]

                password_helper = PasswordHelper()
                hashed_password = password_helper.hash_password(user.password)
                user_uuid = str(uuid.uuid4())
                cursor.execute(query, (user_uuid, user.name, user.email, hashed_password))
                cursor.execute(query_add_role, (user_uuid, user_role_id))

                conn.commit()

                return {"message": "User created successfully"}

        except sqlite3.Error as e:
            logging.error(f"Error creating user: {e}")
            return {"message": f"Error creating user: {e}"}

if __name__ == "__main__":
    user = UserDto(name="tilch", email="GfV2Y@example.com", password="password123")
    print(user)
    user_register = UserRegister()
    user_register.create_user(user)
