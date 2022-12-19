# Fastapi

from fastapi import APIRouter, Response, HTTPException

# Internal Module

from schema.user_schema import UserSchema, DataUser
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
    return {"message": "Fastapi CRUD with SQLalchemy"}


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
    
    
## Simple Login User    
    
@user.post("/api/user/login", status_code = status.HTTP_200_OK)
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        
        # User existence and password validation
        
        if result != None:
            check_passw = check_password_hash(result[3] ,data_user.user_passw)
                  
            if check_passw:
                return {
                    "status": status.HTTP_200_OK,
                    "message": "Access Success"
                }
            
        return {
            "status": status.HTTP_401_UNAUTHORIZED,
            "message": "Access Denied"
        }
            

## Get all users

@user.get("/api/user", response_model = List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()        
        
        return result
    
    
## Get User

@user.get("/api/user/{user_id}", response_model = UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        ### User existence validation and exception
        
        if result != None:            
            return result
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")           
    
    
## Update User

@user.put("/api/user/{user_id}", response_model = UserSchema)
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        
        ### Encrypting password
        
        encrypt_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)
        
        ### Validating user data
        
        #### It's very important to use where() to not modify the entire database
        
        conn.execute(users.update().values(name = data_update.name, username = data_update.username, user_passw = encrypt_passw).where(users.c.id == user_id))
        
        ### The first result of the search is obtained
        
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        return result
    
    
## Delete User

@user.delete("/api/user/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
        
        ### Validating user data
        
        #### It is very important to use where to avoid deleting the database
        
        conn.execute(users.delete().where(users.c.id == user_id))
        
        return Response(status_code = status.HTTP_204_NO_CONTENT)