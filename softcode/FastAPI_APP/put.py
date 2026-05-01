from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User):
    return {
        "message": f"update user {user_id}",
        "user_id": user_id,
        "updated_date": datetime.now(),
            }