from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the blog API"}

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users/{user_id}/blogs", response_model=schemas.BlogOut)
def add_blog(user_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog, user_id)

@app.get("/blogs", response_model=list[schemas.BlogOut])
def list_blogs(db: Session = Depends(get_db)):
    return crud.get_blogs(db)

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    crud.delete_blog(db, blog_id)
    return {"message": "Blog deleted"}
