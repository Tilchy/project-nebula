from pydantic import BaseModel

class Connection(BaseModel):
    id: int
    name: str
    type_of_connection: str
    last_contact: str
    type_of_contact: str
    desired_frequency_of_contact: int
    description: str
    user_uuid: str