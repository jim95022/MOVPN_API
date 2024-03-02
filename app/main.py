from fastapi import FastAPI, HTTPException
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
    try:
        users.add(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))


@app.delete("/users/{username}", status_code=status.HTTP_202_ACCEPTED)
async def add_users(username: str):
    try:
        users.remove(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))
