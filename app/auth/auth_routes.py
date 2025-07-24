from fastapi import APIRouter, Depends, HTTPException
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
