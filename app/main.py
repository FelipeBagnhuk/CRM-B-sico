from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.modelos.clientes import Client
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.rotas.client import router, front_router
from app.rotas.login import router as login_router
from app.rotas.register import router as register_router
from app.rotas.games import router as games_router
from app.config import BASE_DIR
from app.autentication_diddleware import AuthenticationToken

templates = Jinja2Templates(directory=str(BASE_DIR / "templates" / "templates"))

app = FastAPI(
    title="Alura API",
    description="CRM Básico",
    version="1.0.0"
)

app_teste = FastAPI(
    title="Teste API", 
    description="API de teste",
    version="1.0.1"
)



app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static" / "static")), name="static")
app.add_middleware(AuthenticationToken)
app.include_router(router)
app.include_router(front_router)
app.include_router(login_router)
app.include_router(register_router)
app_teste.include_router(games_router)


@app_teste.get("/check_app_status")
async def status_teste():
    return {"status": "Aplicação funcionando!"}  # Comando dentro do main: uvicorn app.main:app_teste --host 0.0.0.0 --port 8001 --reload

#Para acessar a documentação:
#http://localhost:8001/docs#

@app.get("/health")
async def status():
    return {"status": "Ok"}  # Comando: cd CRM-B-sico && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(request, "index.html", {"titulo": "Techlog Solutions CRM", "versao": "1.0.0"})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session_token")
    return response