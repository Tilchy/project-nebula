import jwt
import os

from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone


class Auth():
    def __init__(self):
        load_dotenv()
        self.secret_key = os.getenv('JWT_SECRET')

    def generate_jwt_token(self, user_id: int, expires_in: int):
        """
        Generate a JWT token with an expiration time.
        """
        print(f'User id: {user_id}')
        expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        payload = {
            'user_id': user_id,
            'exp': expiration
        }

        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
    
    def verify_token(self, token: str):
        """
        Verify the JWT token.
        """
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

    def refresh_access_token(self, refresh_token: str):
        """
        Refresh the access token using the refresh token.
        """
        decoded = self.verify_token(refresh_token)
        if 'error' in decoded:
            return decoded

        # Generate a new access token
        new_access_token = self.generate_jwt_token(decoded['user_id'], expires_in=15)  # minutes
        return {
            "access_token": new_access_token
        }