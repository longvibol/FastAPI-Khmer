from fastapi import FastAPI
from homew1 import app as homew1

app = FastAPI()

@app.get("/home")
def home():
    return {"message": "Hello FastAPI!"}

@app.get("/user/{username}")
def user(username: str):
    return {"username": username}

@app.get("/user/{username}/id/{id}")
def user_id(username: str, id: int):
    return {"username": username,
            "id": id}

@app.get("/items/")
def items(limit: int = 10):
    return {"limit": limit}

@app.get("/items1/")
def items(limit: int = 10, id: int = 1):
    return {"limit": limit, "id": id}

@app.get("/search/")
def items(keyword: str = "python"):
    return {"keyword": keyword}


@app.get("/products")
def get_products(limit: int = 2, skip: int = 2):
    return {"limit": limit,
            "skip": skip}

app.mount("/homew1", homew1)