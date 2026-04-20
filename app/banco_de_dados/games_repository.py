from app.banco_de_dados.local import LocationDB
from app.modelos.games import Games, GamesMakeUpdate

class GamesRepository:
    def __init__(self, database: LocationDB):
        self.db = database

    async def list_games(self) -> list[Games]:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, gender from games")
            lines = cursor.fetchall()
            games = [
                Games(id_=line[0], name=line[1], gender=line[2])
                       for line in lines
            ]
            return games
        
    async def get_game(self, game_id:int) -> Games | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, gender FROM games WHERE id = ?" (game_id)
            )
            line = cursor.fetchone()
            if line:
                return Games(id_=line[0], name=line[1], gender=line[2])
            return None
        
    async def make_game(self, game: GamesMakeUpdate) -> Games:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO games (name, gender) VALUES (?,?)", (game.name, game.gender)
                )
            game_id = cursor.lastrowid #Entender posteriormente
            return Games(id_=game_id, name=game.name, gender=game.gender)
        
    async def update_game(self, game_id: int, game: GamesMakeUpdate) -> Games | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE games SET name = ?, gender = ? WHERE id = ?",
                (game.name, game.gender, game_id)
            )
            if cursor.rowcount == 0:
                return None
            return Games(id_=game_id, name=game.name, gender=game.gender)

    async def delete_game(self, game_id: int) -> bool:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM games WHERE id = ?", (game_id,)
            )
            return cursor.rowcount > 0       

