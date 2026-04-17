from pydantic import BaseModel

class Client(BaseModel):
    id_: int 
    name: str
    email: str
    tel: str
 
class ClientMakeUpdate(BaseModel):
    name: str
    email: str
    tel: str