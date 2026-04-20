from app.banco_de_dados.local import LocationDB
from app.modelos.games import Games, GamesMakeUpdate

class ClientRepository:
    def __init__(self, database: LocationDB):
        self.db = database

    async def list_clients(self) -> list[Games]:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, gender from clientes")
            lines = cursor.fetchall()
            games = [
                Games(id_=line[0], name=line[1], gender=line[2])
                       for line in lines
            ]
            return games
        
        #continuar