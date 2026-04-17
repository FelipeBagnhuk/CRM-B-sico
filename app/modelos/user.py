from pydantic import BaseModel

class User(BaseModel):
    id_: int 
    name: str
    email: str
    password: str | None = None
 
class UserMakeUpdate(BaseModel):
    name: str
    email: str
    password: str | None = None