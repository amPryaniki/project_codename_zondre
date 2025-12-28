from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.fake_db import fake_users_db, fake_posts_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")

fake_posts_db = []

def login_required(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/auth/login", status_code=302)
    return request.session["user_id"]

@router.get("/posts", response_class=HTMLResponse)
async def posts_list(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": fake_posts_db})

@router.get("/posts/create", response_class=HTMLResponse)
async def create_post_form(request: Request, user_id: int = Depends(login_required)):
    return templates.TemplateResponse("create_post.html", {"request": request})

@router.post("/posts")
async def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Depends(login_required)):
    if not title.strip() or not content.strip():
        raise HTTPException(status_code=400, detail="Заголовок и текст не могут быть пустыми")
    post = {
        "id": len(fake_posts_db) + 1,
        "title": title,
        "content": content,
        "author": request.session["email"],
        "author_id": user_id
    }
    fake_posts_db.append(post)
    return RedirectResponse(url="/posts", status_code=302)
