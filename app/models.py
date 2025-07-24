from sqlalchemy import Column, String, Float, Boolean
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
