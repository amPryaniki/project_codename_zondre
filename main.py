<<<<<<< HEAD
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, users, posts

app = FastAPI(title="Blog")


app.add_middleware(
    SessionMiddleware,
    secret_key="verysecretkey123",
    max_age=3600
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)  


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts.fake_posts_db})

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/auth/login", status_code=302)
    email = request.session["email"]
    user = users.fake_users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})
=======
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
>>>>>>> 5486783b28b05fd78201a5c5baa7cbdbeb191aef
