import os
import sqlite3
import logging

from ..schemas.role import Role, CreateRole
from ..schemas.user import UserInfo, UserRole

from dotenv import load_dotenv

# Admins can update or delete users.
# Admins can update or delete roles.


# TODO: Implement user management
# Everytime we must check if the user is an admin

class UserManagement():

    def __init__(self):
        load_dotenv()
        self.db_path = os.getenv('DB_NAME')

    def check_if_user_is_admin(self, user_uuid: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT role_id FROM user_roles WHERE user_uuid = ?"
                cursor.execute(query, (user_uuid,))
                result = cursor.fetchone()

                cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
                admin_role_id = cursor.fetchone()[0]

                if result and result[0] == admin_role_id:
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            logging.error(f"Error checking if user is admin: {e}")
            return False

    def list_users(self) -> list:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """SELECT users.uuid, users.name, users.email, roles.name
                           FROM users
                           INNER JOIN user_roles ON users.uuid = user_roles.user_uuid
                           INNER JOIN roles ON user_roles.role_id = roles.id
                """
                cursor.execute(query)
                result = cursor.fetchall()

                users = []
                for user in result:
                    user_obj = UserRole(uuid=user[0], name=user[1], email=user[2], role=user[3])
                    users.append(user_obj)

                return users
        except sqlite3.Error as e:
            logging.error(f"Error listing users: {e}")
            return []
        
    def get_user_by_uuid(self, user_uuid: str) -> UserInfo:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """SELECT users.uuid, users.name, users.email, roles.name
                           FROM users
                           INNER JOIN user_roles ON users.uuid = user_roles.user_uuid
                           INNER JOIN roles ON user_roles.role_id = roles.id
                           WHERE users.uuid = ?
                """
                cursor.execute(query, (user_uuid,))
                result = cursor.fetchone()

                if result:
                    return UserInfo(uuid=result[0], name=result[1], email=result[2], role=result[3])

        except sqlite3.Error as e:
            logging.error(f"Error getting user by uuid: {e}")
            return None
        
    def delete_user(self, user_uuid: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "DELETE FROM users WHERE uuid = ?"
                cursor.execute(query, (user_uuid,))
                conn.commit()

                return {"message": f"User {user_uuid} was successfully deleted!"}
        except sqlite3.Error as e:
            logging.error(f"Error deleting user: {e}")
            return {"error": f"Error deleting user: {e}"}
        
    def list_roles(self) -> list:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM roles"
                cursor.execute(query)
                result = cursor.fetchall()

                roles = []
                for role in result:
                    role_obj = Role(id=role[0], name=role[1])
                    roles.append(role_obj)

                return roles
        except sqlite3.Error as e:
            logging.error(f"Error listing roles: {e}")
            return []
        
    def create_role(self, role: CreateRole):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM roles WHERE name = ?"
                cursor.execute(query, (role.name,))
                result = cursor.fetchone()
                if result:
                    logging.error(f"Role with name {role.name} already exists")
                    return {"error": f"Role with name {role.name} already exists"}
        except sqlite3.Error as e:
            logging.error(f"Error checking if role exists: {e}")
            return {"error": f"Error checking if role exists: {e}"}

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "INSERT INTO roles (name) VALUES (?)"
                cursor.execute(query, (role.name,))
                conn.commit()

                return {"message": f"role {role.name} was successfully created!"}
        except sqlite3.Error as e:
            logging.error(f"Error creating role: {e}")
            return {"error": f"Error creating role: {e}"}
        
    def update_role_of_user(self, user_uuid: str, role: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "UPDATE user_roles SET role_id = ? WHERE uuid = ?"
                cursor.execute(query, (role, user_uuid))
                conn.commit()

                return {"message": f"Role of user {user_uuid} was successfully updated to {role}!"}
        except sqlite3.Error as e:
            logging.error(f"Error updating role of user: {e}")
            return {"error": f"Error updating role of user: {e}"}   
         
    def delete_role(self, role_id: int):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM user_roles WHERE role_id = ?"
                cursor.execute(query, (role_id,))
                result = cursor.fetchone()
                if result:
                    logging.error(f"Role is used by user: {result}")
                    return {"error": f"Role is used by user: {result}"}
        except sqlite3.Error as e:
            logging.error(f"Error checking if role is used: {e}")
            return {"error": f"Error checking if role is used: {e}"}

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "DELETE FROM roles WHERE id = ?"
                cursor.execute(query, (role_id,))
                conn.commit()

                return {"message": f"Role {role_id} was successfully deleted!"}
        except sqlite3.Error as e:
            logging.error(f"Error deleting role: {e}")
            return {"error": f"Error deleting role: {e}"}

if __name__ == "__main__":
    user_management = UserManagement()
    print(user_management.list_users())