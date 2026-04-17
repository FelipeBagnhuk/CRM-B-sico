from typing import Annotated

from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.banco_de_dados import user_repository
from app.config import BASE_DIR
from app.modelos.user import UserMakeUpdate
from app.banco_de_dados.client_repository import ClientRepository
from app.depends import get_client_repository, get_user_repository

router = APIRouter(
    prefix="/registro"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates" / "templates"))

@router.get("/", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "registro.html", {"request": request})

@router.post("/")
async def user_register(
    user_repository: Annotated[user_repository.UserRepository, Depends(get_user_repository)],
    request: Request,
    nome = Form(...),
    email = Form(...),
    senha = Form(...),
    confirma_senha = Form(...),
):
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha, 
    }
    

    if not all([email, senha, nome, confirma_senha]):
        return templates.TemplateResponse("registro.html", {"request": request, "error":"Campos Obrigatórios Faltantes", **data})

    if senha != confirma_senha:
        return templates.TemplateResponse("registro.html", {"request": request, "error":"Senhas não coincidem", **data})

    user_exist = await user_repository.get_user_email(email)
    
    if user_exist: 
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "Email já cadastrado!",
            **data
        })

    user_make = UserMakeUpdate(name=nome, email=email, password=senha)
    user = await user_repository.make_user(user_make)

    if user:
        response = RedirectResponse(url="/login", status_code=303)
        return response
    