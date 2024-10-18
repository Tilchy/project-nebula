from pydantic import BaseModel

class Role(BaseModel):
    id: int
    name: str

class CreateRole(BaseModel):
    name: str

class DeleteRole(BaseModel):
    id: int