from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db.fake_db import fake_users_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/auth/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/auth/register")
async def register(
    request: Request,
    email: str = Form(...),
    login: str = Form(...),
    password: str = Form(...)):
    if not email or not login or not password:
        raise HTTPException(status_code=400, detail="Все поля обязательны")
    if email in fake_users_db:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    fake_users_db[email] = {
        "id": len(fake_users_db) + 1,
        "email": email,
        "login": login,
        "password": password
    }
    request.session["user_id"] = fake_users_db[email]["id"]
    request.session["email"] = email
    return RedirectResponse(url="/", status_code=302)
