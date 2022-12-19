# Fastapi

from fastapi import FastAPI

# Internal Functions

from router.router import user


app = FastAPI()


app.include_router(user)
