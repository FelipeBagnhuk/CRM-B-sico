from typing import Annotated

from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config import BASE_DIR
from app.modelos.games import Games, GamesMakeUpdate
from app.banco_de_dados.games_repository import GamesRepository
from app.depends import get_game_repository

router = APIRouter(
    prefix="/api/games"
)

@router.get("", response_model=list[Games])
async def game_list(client_repository: Annotated[GamesRepository, Depends(get_game_repository)]):
    return await client_repository.list_games()

@router.get("/{game_id}", response_model=Games)
async def get_games_id(
    client_id: int,
    game_repository: Annotated[GamesRepository, Depends(get_game_repository)]
):
    game = await game_repository.get_game(client_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game não encontrado")
    return game

@router.post("", response_model=Games)
async def make_game(
    game_repository: Annotated[GamesRepository, Depends(get_game_repository)],
    game: GamesMakeUpdate
):
    return await game_repository.make_game(game)

@router.put("/{game_id}", response_model=Games | None)
async def update_client(
    game_repository: Annotated[GamesRepository, Depends(get_game_repository)],
    game_id: int,
    game: GamesMakeUpdate
):
    updated_game = await game_repository.update_game(game_id, game)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Jogo não encontrado!")
    return updated_game

@router.delete("/{game_id}", status_code=204)
async def delete_game(
    game_repository: Annotated[GamesRepository, Depends(get_game_repository)],
    game_id:int
):
    success = await game_repository.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")