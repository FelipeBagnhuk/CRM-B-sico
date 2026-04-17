from typing import Annotated

from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.banco_de_dados import user_repository
from app.config import BASE_DIR
from app.modelos.clientes import Client, ClientMakeUpdate
from app.banco_de_dados.client_repository import ClientRepository
from app.depends import get_client_repository, get_user_repository

router = APIRouter(
    prefix="/login"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates" / "templates"))

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@router.post("/")
async def login(
    request: Request,
    user_repository: Annotated[user_repository.UserRepository, Depends(get_user_repository)],
    email: str = Form(...),
    password: str = Form(...)
):
    user = await user_repository.get_users_for_email_password(email, password)
    if user:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="toke-password", httponly=True)
        return response
    
    return templates.TemplateResponse(request, "login.html", {
        "request": request,
        "email": email,
        "password": password,
        "error": "Credenciais inválidas!"
    })


    