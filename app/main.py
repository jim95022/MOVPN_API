from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

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


@app.get("/users/{username}/qr")
async def retrieve_users(username: str):
    filename = f"{username}.png"
    try:
        qr_code_path = users.get_cred_path(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} is not exists")
    return FileResponse(
        path=qr_code_path,
        filename=filename,
        media_type='multipart/form-data'
    )


@app.get("/users/{username}/conf")
async def retrieve_users(username: str):
    filename = f"{username}.conf"
    try:
        conf_path = users.get_cred_path(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} is not exists")
    return FileResponse(
        path=conf_path,
        filename=filename,
        media_type='multipart/form-data'
    )


@app.delete("/users/{username}", status_code=status.HTTP_202_ACCEPTED)
async def remove_users(username: str):
    try:
        users.remove(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))
