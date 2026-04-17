from typing import Annotated

from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import BASE_DIR
from app.modelos.clientes import Client, ClientMakeUpdate
from app.banco_de_dados.client_repository import ClientRepository
from app.depends import get_client_repository

templates = Jinja2Templates(directory=str(BASE_DIR / "templates" / "templates"))

router = APIRouter(
    prefix="/api/clients"
)

front_router = APIRouter(
    prefix="/clientes"
)


@router.get("", response_model=list[Client])
async def clients_list(client_repository: Annotated[ClientRepository, Depends(get_client_repository)]):
    return await client_repository.list_clients()

@router.get("/{client_id}", response_model=Client)
async def get_client_id(
    client_id: int,
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)]
):
    client = await client_repository.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.post("", response_model=Client)
async def make_client(
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
    client: ClientMakeUpdate
):
    return await client_repository.make_client(client)

@router.put("/{client_id}", response_model=Client | None)
async def update_client(
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
    client_id: int,
    client: ClientMakeUpdate
):
    updated_client = await client_repository.update_client(client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    return updated_client

@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
    client_id:int
):
    success = await client_repository.delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
@front_router.get("/", response_class=HTMLResponse)
async def page_list_clients(request: Request, client_repository: Annotated[ClientRepository, Depends(get_client_repository)]):
    clientes = await client_repository.list_clients()
    return templates.TemplateResponse(request, "clientes.html", {"request": request, "clientes": clientes, "titulo": "Lista de Clientes"})

@front_router.get("/novo", response_class=HTMLResponse)
async def page_make_client(request: Request):
    return templates.TemplateResponse(request, "clientes-form.html", {"request": request, "cliente": None, "cliente_id": None})

@front_router.get("/{client_id}", response_class=HTMLResponse)
async def page_edit_client(
    request: Request,
    client_id: int,
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)]
):
    cliente = await client_repository.get_client(client_id)
    return templates.TemplateResponse(request, "clientes-form.html", {"request": request, "cliente": cliente, "cliente_id": client_id})