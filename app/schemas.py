from pydantic import BaseModel
from uuid import UUID

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    em_estoque: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: UUID
    class Config:
        orm_mode = True

class UsuarioCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
