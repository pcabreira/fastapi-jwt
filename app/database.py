from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
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
