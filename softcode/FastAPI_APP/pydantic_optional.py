from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    username: str
    age: int
    gmail: Optional[str] = None

@app.post("/users/")
def create_user(user: User):
    if user.gmail:
        return {"Gmail": user.gmail}
    else:
        return {"No Email: ": "No Email !"}

@app.put("/users/{id}")
def update_user(id: int, user: User):
    return {"id": id, "username": user.username, "age": user.age}
