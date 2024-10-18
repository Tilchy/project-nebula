from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    uuid: str
    name: str
    email: EmailStr
    password: str

class UserDto(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLoginDto(BaseModel):
    email: EmailStr
    password: str

class UserRegisterDto(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    uuid: str
    name: str
    email: EmailStr

class UserRole(BaseModel):
    uuid: str
    name: str
    email: EmailStr
    role: str