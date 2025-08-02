from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return "Welcome to FastAPI!"

@app.get("/hello")
def hello():
    return  "hi there!"

@app.get("/status/")
def status():
    return {"status": "running", "version": "1.0.0"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/feedback")
def feedback(name: str, message: str):
    return {f"Feedback received from {name}: {message}"}

@app.get("/search/")
def search_items(q: str = None):
    return {"query": q}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id,"active": True}

@app.get("/blog/{blog_id}")
def read_blog(blog_id: int, comments: Optional[str] = None):
    return {"blog_id": blog_id, "comments": comments}

class Product(BaseModel):
    name:str
    price:str
    in_stock:bool = True

@app.post("/add_product")
def add_product(product: Product):
    return {
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock
    }

class Blog(BaseModel):
    title: str
    content: Optional[str]
    published: bool = True

@app.post("/create-blog")
def create_blog(blog: Blog):
    return {
        "title": blog.title,
        "content": blog.content,
        "published": blog.published
    }


#nested models example
class Author(BaseModel):
    name: str
    email: str

class Blog(BaseModel):
    title: str
    content: str
    author: Author

@app.post("/create-blog-with-author")
def create_blog_with_author(blog: Blog):
    return {
        "title": blog.title,
        "content": blog.content,
        "author": {
            "name": blog.author.name,
            "email": blog.author.email
        }
    }

#form data example
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "message": "Login successful"}

#file upload example
@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "content_type": file.content_type}

@app.post("/upload-multiple/")
def upload_multiple_files(files: list[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files], "count": len(files)}

#form data with file upload example
@app.post("/register/")
def register(name: str = Form(...), email: str = Form(...)):
    return {"name": name, "email": email, "message": "Registration successful"}

@app.post("/profile-pic")
def upload_profile_pic(photo: UploadFile = File(jpg=True)):
    return {"filename": photo.filename, "content_type": photo.content_type}

# #response model example
# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserOut(BaseModel):
#     username: str
#     email: str

# @app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# def register_user(user: User):
#     return user


#dependency using class
class Settings:
    def __init__(self):
        self.api_key = "super-secret"

@app.get("/config")
def get_config(settings: Settings = Depends(Settings)):
    return {"api_key": settings.api_key}


