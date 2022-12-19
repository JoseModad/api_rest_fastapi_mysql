# Fastapi

from fastapi import APIRouter

# Internal Module

from schema.user_schema import UserSchema
from config.db import conn
from model.users import users

# Werkzeug

from werkzeug.security import generate_password_hash, check_password_hash


user = APIRouter()


@user.get("/")
def root():
    return {"message": "Hi I am Fastapi"}


@user.post("/api/user")
def create_user(data_user: UserSchema):
    new_user = data_user.dict()
    new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
    conn.execute(users.insert().values(new_user))    
    return "Success"
    