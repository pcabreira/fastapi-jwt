from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.schemas import ProdutoCreate, Produto
from app.models import Produto as ProdutoModel
from app.database import SessionLocal
from app.core.security import verificar_token_api_key  # ✅ novo import

router = APIRouter()

# Dependência de sessão com banco
async def get_db():
    async with SessionLocal() as session:
        yield session

# ✅ Rota protegida por token
@router.get("/", response_model=list[Produto])
async def listar(
    db: AsyncSession = Depends(get_db),
    usuario: str = Depends(verificar_token_api_key)
):
    result = await db.execute(select(ProdutoModel))
    return result.scalars().all()

@router.post("/", response_model=Produto)
async def criar(
    prod: ProdutoCreate,
    db: AsyncSession = Depends(get_db),
    usuario: str = Depends(verificar_token_api_key)
):
    novo = ProdutoModel(**prod.dict())
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo

@router.get("/{produto_id}", response_model=Produto)
async def get(
    produto_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: str = Depends(verificar_token_api_key)
):
    result = await db.execute(select(ProdutoModel).filter_by(id=produto_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return item

@router.delete("/{produto_id}")
async def delete(
    produto_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: str = Depends(verificar_token_api_key)
):
    result = await db.execute(select(ProdutoModel).filter_by(id=produto_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await db.delete(item)
    await db.commit()
    return {"msg": "Produto deletado com sucesso"}
