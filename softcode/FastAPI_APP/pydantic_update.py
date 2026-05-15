from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=0, lt=120)
    gmail: str = Field(pattern=r"^[\w\.-]+@gmail\.com$")

@app.post("/users/")
def create_user(user: User):
    return user
