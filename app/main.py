from fastapi import FastAPI
from starlette import status

from app.users import UsersProcessor
from settings import CONFIG_FILE

app = FastAPI()
users = UsersProcessor(config_file=CONFIG_FILE, config_folder="")


@app.get("/users")
async def get_users():
    all_users = users.get()
    return {"users": all_users}


@app.post("/users/{username}", status_code=status.HTTP_201_CREATED)
async def add_users(username: str):
    users.add(username)
