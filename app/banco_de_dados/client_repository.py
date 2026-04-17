from app.banco_de_dados.local import LocationDB
from app.modelos.clientes import Client, ClientMakeUpdate

class ClientRepository:
    def __init__(self, database: LocationDB):
        self.db = database

    async def list_clients(self) -> list[Client]:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, email, tel from clientes")
            lines = cursor.fetchall()
            clients = [
                Client(id_=line[0], name=line[1], email=line[2], tel=line[3])
                       for line in lines
            ]
            return clients

    async def get_client(self, client_id: int) -> Client | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, email, tel FROM clientes WHERE id = ?", (client_id,)
                )
            line = cursor.fetchone()
            if line:
                return Client(id_=line[0], name=line[1], email=line[2], tel=line[3])
            return None
        
    async def make_client(self, client: ClientMakeUpdate) -> Client:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO clientes (name, email, tel) VALUES (?,?,?)", (client.name, client.email, client.tel)
                )
            client_id = cursor.lastrowid
            return Client(id_=client_id, name=client.name, email=client.email, tel=client.tel)

    async def update_client(self, client_id: int, client: ClientMakeUpdate) -> Client | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE clientes SET name = ?, email = ?, tel = ? WHERE id = ?",
                (client.name, client.email, client.tel, client_id)
            )
            if cursor.rowcount == 0:
                return None
            return Client(id_=client_id, name=client.name, email=client.email, tel=client.tel)
        
    async def delete_client(self, client_id: int) -> bool:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM clientes WHERE id = ?", (client_id,)
            )
            return cursor.rowcount > 0