import sqlite3
from contextlib import contextmanager

class LocationDB():
    def __init__(self, file_name="alura.db"):
        self.file_name = file_name
        self.start_db()

    @contextmanager
    def conect(self):
        connection = sqlite3.connect(self.file_name)
        try:
            yield connection
            connection.commit() #faz commit se dá certo
        except Exception as e:
            connection.rollback() #faz rollback se dá errado
            raise e
        finally:
            connection.close()       

    def start_db(self):
        with self.conect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    tel TEXT NOT NULL
    )
""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
    )
""")
            # Check if password column exists, if not, add it
            cursor.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'password' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN password TEXT NOT NULL DEFAULT ''")
        print("Banco de dados inicializado")            
