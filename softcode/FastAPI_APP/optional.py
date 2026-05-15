from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

@app.post("/register/")
def register(user: User):
    if user.email:
        return {"message": f"register name {user.name} with email {user.email}"}
    else:
        return {"message": f"register name {user.name}"}