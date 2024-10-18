import random
import string
import bcrypt

class PasswordHelper:
    @staticmethod
    def generate_password(length):
        allowed_characters = (
            string.ascii_uppercase.replace('I', '').replace('O', '') +
            string.ascii_lowercase.replace('l', '') + 
            string.digits.replace('1', '').replace('0', '') +                          
            '!.-_ '                        
        )

        password = ''.join(random.choice(allowed_characters) for _ in range(length))
        return password

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

if __name__ == "__main__":
    password_helper = PasswordHelper()
    password = password_helper.generate_password(10)
    hashed_password = password_helper.hash_password(password)
    print(f"Generated Password: {password}")
    print(f"Hashed Password: {hashed_password}")
    print(f"Password Verified: {password_helper.verify_password(password, hashed_password)}")