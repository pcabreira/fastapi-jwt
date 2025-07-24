from fastapi import FastAPI
from app.routes import products
from app.auth import auth_routes
from app.database import create_db

app = FastAPI(title="API Produtos com JWT")

app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products.router, prefix="/produtos", tags=["Produtos"])

@app.on_event("startup")
async def startup():
    await create_db()