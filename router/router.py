# Fastapi

from fastapi import APIRouter, Response

# Internal Module

from schema.user_schema import UserSchema
from config.db import engine
from model.users import users

# Werkzeug

from werkzeug.security import generate_password_hash, check_password_hash

# Starlette

from starlette import status

# Typing

from typing import List


user = APIRouter()

# Routes

## Home 

@user.get("/")
def root():
    return {"message": "Hi I am Fastapi"}


## Create User

@user.post("/api/user", status_code = status.HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        
        # Encryption 
        
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        
        # Writing to database
        
        conn.execute(users.insert().values(new_user))    
        return Response(status_code = status.HTTP_201_CREATED)


## Get all users

@user.get("/api/user", response_model = List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result
    
    
# Get User

@user.get("/api/user/{user_id}", response_model = UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        return result
    
    
# Update User

@user.put("/api/user/{user_id}")
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encrypt_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)
        conn.execute(users.update().values(name = data_update.name, username = data_update.username, user_passw = encrypt_passw).where(users.c.id == user_id))
        
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        return result