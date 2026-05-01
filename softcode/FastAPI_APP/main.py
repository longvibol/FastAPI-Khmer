from fastapi import FastAPI
from homew1 import app as homew1  # import homew1 app

app = FastAPI()

app.mount("/", homew1)

@app.get("/")
def home():
    return {"message": "Hello FastAPI!"}

#with one parameter
@app.get("/user/{username}")
def user(username: str):
    return {"username": username}

#with multiple parameter
@app.get("/user/{username}/id/{id}")
def user_id(username: str, id: int):
    return {"username": username, "id": id}

#query
@app.get("/items/")
def items(limit: int = 10, user_id:int = 2):
    return {"limit": limit, "user_id": user_id }

@app.get("/products")
def get_products(limit: int = 2, skip: int = 2):
    return {"limit": limit, "skip": skip}