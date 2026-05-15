from fastapi import FastAPI

app = FastAPI()

@app.get("/hw/home/")
def home():
    return {"message": "Hello world"}

@app.get("/hw/students/{id}")
def user(id : int):
    return {"student_id": id}

#with multiple parameter
@app.get("/hw/search/")
def user_id(keyword: str = "python"):
    return {"keyword": keyword}