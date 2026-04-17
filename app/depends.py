from typing import Annotated
from fastapi import Depends

from app.banco_de_dados.local import LocationDB
from app.banco_de_dados.client_repository import ClientRepository
from app.banco_de_dados.user_repository import UserRepository


banco_de_dados = LocationDB()

def get_db() -> LocationDB:
    return banco_de_dados

def get_client_repository(banco_de_dados_local: Annotated[LocationDB, Depends(get_db)]) -> ClientRepository:
    return ClientRepository(banco_de_dados_local)

def get_user_repository(
        banco_de_dados_local: Annotated[LocationDB, Depends(get_db)]
) -> UserRepository:
    
    return UserRepository(banco_de_dados_local)