from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime

app = FastAPI()

class User(BaseModel):
    id: int
    email: EmailStr
    login: str
    password: str
    createdAt: datetime
    updatedAt: datetime

class Post(BaseModel):
    id: int
    authorId: int
    title: str
    content: str
    createdAt: datetime
    updatedAt: datetime

users = {}
posts = {}

#чето
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    users[user.id] = user
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"detail": "User deleted"}

#чето 2
@app.post("/posts/", response_model=Post)
async def create_post(post: Post):
    if post.id in posts:
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    if post.authorId not in users:
        raise HTTPException(status_code=404, detail="Author not found")
    posts[post.id] = post
    return post

@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[post_id]

@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, updated_post: Post):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    if updated_post.authorId not in users:
        raise HTTPException(status_code=404, detail="Author not found")
    posts[post_id] = updated_post
    return updated_post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]
    return {"detail": "Post deleted"}
