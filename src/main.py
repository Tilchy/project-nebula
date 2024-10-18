from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated

from .schemas.user import UserLoginDto, UserDto
from .users.login import UserLogin
from .users.register import UserRegister
from .users.auth import Auth
from .users.user_management import UserManagement
from .utils.password import PasswordHelper
app = FastAPI()
security = HTTPBearer()

@app.get("/")
async def read_root():
    return {"Go to /docs, for more information"}

@app.post("/generate-password")
async def generate_password():
    return PasswordHelper.generate_password(10)

@app.post("/register")
async def register(user: UserDto):
    user_register = UserRegister()
    return user_register.create_user(user)

@app.post("/login")
async def login(user: UserLoginDto):
    user_login = UserLogin()
    return user_login.login_user(user.email, user.password)

@app.post("/token/refresh")
async def refresh_token(refresh_token: str):
    auth = Auth()
    return auth.refresh_access_token(refresh_token)

@app.post("/token/verify")
async def verify_token(token: str):
    auth = Auth()
    return auth.verify_token(token)

@app.get("/user/roles")
async def get_roles(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    auth = Auth()
    is_valid = auth.verify_token(credentials.credentials)

    if 'error' in is_valid:
        return is_valid

    user_management = UserManagement()

    if not user_management.check_if_user_is_admin(is_valid['user_id']):
        return {"error": "You do not have permission to list users."}
    
    return user_management.list_roles()