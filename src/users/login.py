import os
import sqlite3
import logging

from .auth import Auth
from ..utils.password import PasswordHelper
from ..schemas.user import User, UserDto, UserInfo
from dotenv import load_dotenv


class UserLogin():

    def __init__(self):
        load_dotenv()
        self.db_path = os.getenv('DB_NAME')

    def get_user_from_db(self, email: str) -> User:
        """
        Retrieve a user by email from the database.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT id, uuid, name, email, password FROM users WHERE email = ?"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    return User(id=result[0], uuid=result[1], name=result[2], email=result[3], password=result[4])
                else:
                    return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        

    def login_user(self, email: str, password: str):
            """
            Log the user in by verifying credentials and returning a JWT access token.
            """
            user = self.get_user_from_db(email)
            if user is None:
                return {"error": "User does not exist"}

            password_helper = PasswordHelper()
            if not password_helper.verify_password(password, user.password):
                return {"error": "Incorrect password"}

            auth = Auth()
            access_token = auth.generate_jwt_token(user.uuid, expires_in=15)  # 15 minutes expiry
            refresh_token = auth.generate_jwt_token(user.uuid, expires_in=1440)  # 24 hours expiry
            
            userInfo = UserInfo(uuid=user.uuid, name=user.name, email=user.email)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": userInfo
            }
    

if __name__ == "__main__":
    user = UserDto(name="tilen", email="tilen@test.com", password="password123")
    login = UserLogin()
    user_login = login.login_user(user.email, user.password)