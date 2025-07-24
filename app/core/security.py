from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM

# 🔒 Usando HTTPBearer (Swagger já adiciona "Bearer " automaticamente)
http_bearer = HTTPBearer(auto_error=True)

async def verificar_token_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    token = credentials.credentials  # Já extrai só o token (sem "Bearer ")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
