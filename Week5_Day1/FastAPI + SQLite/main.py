from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal

#create tables
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/users/", response_model= schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.userRespones])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.put("/user/{user_id}", response_model=schemas.userRespones)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "message": "User deleted successfully"
    }