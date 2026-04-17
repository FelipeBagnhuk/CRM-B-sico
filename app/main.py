from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.modelos.clientes import Client
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.rotas.client import router, front_router
from app.rotas.login import router as login_router
from app.rotas.register import router as register_router
from app.config import BASE_DIR
from app.autentication_diddleware import AuthenticationToken

templates = Jinja2Templates(directory=str(BASE_DIR / "templates" / "templates"))

app = FastAPI(
    title="Alura API",
    description="CRM Básico",
    version="1.0.0"
)



app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static" / "static")), name="static")
app.add_middleware(AuthenticationToken)
app.include_router(router)
app.include_router(front_router)
app.include_router(login_router)
app.include_router(register_router)




@app.get("/health")
async def status():
    return {"status": "Ok"}


@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(request, "index.html", {"titulo": "Techlog Solutions CRM", "versao": "1.0.0"})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session_token")
    return response