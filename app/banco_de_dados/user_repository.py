from app.banco_de_dados.local import LocationDB
from app.modelos.user import User, UserMakeUpdate

class UserRepository:
    def __init__(self, database: LocationDB):
        self.db = database

    async def get_users_for_email_password(self, email: str, password: str) -> User | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE email = ? AND password = ?", (email, password))
            line = cursor.fetchone()
            if line:
                return User(id_=line[0], name=line[1], email=line[2])
            return None
        
    async def make_user(self, user_make: UserMakeUpdate) -> User:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (user_make.name, user_make.email, user_make.password)
            )
            id_ = cursor.lastrowid
            return User(id_=id_, name=user_make.name, email=user_make.email)
        
    async def get_user_email(self, email: str) -> User | None:
        with self.db.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE email = ?", (email,))
            line = cursor.fetchone()
            if line:
                return User(id_=line[0], name=line[1], email=line[2])
            return None