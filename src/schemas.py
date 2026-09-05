from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    senha : str
    nome : str

    class Config:
        from_attributes = True