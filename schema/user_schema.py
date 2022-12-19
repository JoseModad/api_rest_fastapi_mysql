# Pydantic

from pydantic import BaseModel
from typing import Optional


# Class

class UserSchema(BaseModel):
    
    # The id will be generated automatically in the database
    
    id: Optional[str]
    name: str
    username: str
    user_passw: str



class DataUser(BaseModel):
    username: str
    user_passw: str