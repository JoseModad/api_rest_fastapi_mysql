# Fastapi

from fastapi import APIRouter, Response

# Internal Module

from schema.user_schema import UserSchema
from config.db import conn
from model.users import users

# Werkzeug

from werkzeug.security import generate_password_hash, check_password_hash

# Starlette

from starlette import status


user = APIRouter()

# Routes

## Home 

@user.get("/")
def root():
    return {"message": "Hi I am Fastapi"}


## Create User

@user.post("/api/user", status_code = status.HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    new_user = data_user.dict()
    
    # Encryption 
    
    new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
    
    # Writing to database
    
    conn.execute(users.insert().values(new_user))    
    return Response(status_code = status.HTTP_201_CREATED)
    