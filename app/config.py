import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
