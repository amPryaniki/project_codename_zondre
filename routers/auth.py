from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db.fake_db import fake_users_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def login_required(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/auth/login", status_code=302)
    return request.session["user_id"]

@router.get("/auth/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/auth/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)):
    user = fake_users_db.get(email)
    if user and user["password"] == password:
        request.session["user_id"] = user["id"]
        request.session["email"] = user["email"]
        return RedirectResponse(url="/", status_code=302)
    raise HTTPException(status_code=401, detail="Неверный email или пароль")

@router.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)
