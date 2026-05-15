from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    age: int
    gmail: str

@app.post("/users/")
def create_user(user: User):
    return {"username": user.username,
            "age": user.age,
            "gmail": user.gmail
            }
