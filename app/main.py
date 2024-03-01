from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
async def get_users():
    return {"users": ["phone", "laptop", "desktop"]}
