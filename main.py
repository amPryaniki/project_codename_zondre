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
