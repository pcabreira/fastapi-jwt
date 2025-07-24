import os

# Estrutura de diretórios
structure = {
    "app": {
        "__init__.py": "",
        "main.py": """from fastapi import FastAPI
from app.routes import products
from app.auth import auth_routes
from app.database import create_db

app = FastAPI(title="API Produtos com JWT")

app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products.router, prefix="/produtos", tags=["Produtos"])

@app.on_event("startup")
async def startup():
    await create_db()
""",
        "config.py": """import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
""",
        "database.py": """from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

DATABASE_URL_ASYNC = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def create_db():
    async with engine.begin() as conn:
        import app.models  # necessário para registrar modelos
        await conn.run_sync(Base.metadata.create_all)
""",
        "models.py": """from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    em_estoque = Column(Boolean, default=True)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
""",
        "schemas.py": """from pydantic import BaseModel
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
""",
        "auth": {
            "__init__.py": "",
            "auth_routes.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UsuarioCreate, Token
from app.models import Usuario
from app.database import SessionLocal
from passlib.context import CryptContext
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

async def get_db():
    async with SessionLocal() as session:
        yield session

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/registro")
async def registrar(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    result = await db.execute(select(Usuario).filter(Usuario.username == user.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Usuário já existe")
    novo = Usuario(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(novo)
    await db.commit()
    return {"msg": "Usuário criado com sucesso"}

@router.post("/login", response_model=Token)
async def login(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    result = await db.execute(select(Usuario).filter(Usuario.username == user.username))
    usuario = result.scalar()
    if not usuario or not verify_password(user.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}
""",
        },
        "routes": {
            "__init__.py": "",
            "products.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import ProdutoCreate, Produto
from app.models import Produto as ProdutoModel
from app.database import SessionLocal
from sqlalchemy.future import select
from uuid import UUID

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[Produto])
async def listar(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProdutoModel))
    return result.scalars().all()

@router.post("/", response_model=Produto)
async def criar(prod: ProdutoCreate, db: AsyncSession = Depends(get_db)):
    novo = ProdutoModel(**prod.dict())
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo

@router.get("/{produto_id}", response_model=Produto)
async def get(produto_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProdutoModel).filter_by(id=produto_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return item

@router.delete("/{produto_id}")
async def delete(produto_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProdutoModel).filter_by(id=produto_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await db.delete(item)
    await db.commit()
    return {"msg": "Produto deletado com sucesso"}
"""
        }
    },
    "Dockerfile": """FROM python:3.11-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yml": """version: '3.9'

services:
  web:
    build: .
    container_name: fastapi_app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
      - SECRET_KEY=chave-super-secreta

  db:
    image: postgres:13
    container_name: fastapi_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
""",
    "requirements.txt": """fastapi
uvicorn[standard]
sqlalchemy
asyncpg
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
"""
}

# Criação de arquivos e pastas
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ Projeto gerado com sucesso!")
