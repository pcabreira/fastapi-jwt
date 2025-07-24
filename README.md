API de Cadastro de Usuários e Produtos com JWT

````markdown
# 🚀 API de Cadastro de Usuários e Produtos

Uma API RESTful simples desenvolvida com **FastAPI**, que permite:

- 📦 Cadastro, listagem e exclusão de **produtos**
- 👤 Cadastro e autenticação de **usuários**
- 🔐 Proteção de rotas com **JWT (Bearer Token)**
- 🐘 Persistência com **PostgreSQL**
- 🐳 Execução via **Docker e Docker Compose**

---

## ✅ Funcionalidades

- [x] Registro e login de usuários com senha criptografada
- [x] Emissão de token JWT na autenticação
- [x] Proteção de rotas com autenticação via `Bearer Token`
- [x] CRUD de produtos
- [x] Swagger UI com suporte automático a token
- [x] Banco de dados PostgreSQL com SQLAlchemy (assíncrono)
- [x] Deploy local com Docker

---

## 🧱 Tecnologias Utilizadas

| Tecnologia    | Uso Principal                  |
|---------------|--------------------------------|
| FastAPI       | Framework web assíncrono       |
| PostgreSQL    | Banco de dados relacional      |
| Docker        | Containerização da aplicação   |
| SQLAlchemy    | ORM com suporte a async        |
| python-jose   | Geração e validação de JWT     |
| Passlib       | Criptografia de senhas         |
| Uvicorn       | Servidor ASGI para FastAPI     |

---

## 🐳 Executando com Docker

### 1. Clone o repositório

```bash
git clone https://github.com/pcabreira/fastapi-jwt.git
cd fastapi-jwt
````

### 2. Suba os containers

```bash
docker-compose up --build
```

A API estará disponível em:
➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Documentação e Testes via Swagger

Acesse a documentação interativa em:

```
http://localhost:8000/docs
```

Use o botão **Authorize**, cole o token JWT e use as rotas protegidas.

---

## 🔐 Autenticação com JWT

### 1. Registro

```http
POST /auth/registro
{
  "username": "joao",
  "password": "123456"
}
```

### 2. Login

```http
POST /auth/login
{
  "username": "joao",
  "password": "123456"
}
```

Retorno:

```json
{
  "access_token": "jwt.token.aqui",
  "token_type": "bearer"
}
```

### 3. Usar no Swagger UI

Clique em "Authorize" e cole **apenas o token**, sem precisar digitar `Bearer` manualmente. O Swagger já adiciona o prefixo.

---

## 📦 Rotas da API

### 🔓 Público

| Método | Rota             | Descrição                |
| ------ | ---------------- | ------------------------ |
| POST   | `/auth/registro` | Cadastro de novo usuário |
| POST   | `/auth/login`    | Login e geração do token |

### 🔐 Protegido (requer token JWT)

| Método | Rota             | Descrição                |
| ------ | ---------------- | ------------------------ |
| GET    | `/produtos/`     | Listar todos os produtos |
| POST   | `/produtos/`     | Criar novo produto       |
| GET    | `/produtos/{id}` | Buscar produto por ID    |
| DELETE | `/produtos/{id}` | Remover produto por ID   |

---

## ⚙️ Variáveis de Ambiente

Crie um `.env` (exemplo):

```env
POSTGRES_DB=fastapi_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_pass
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_pass@db:5432/fastapi_db

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
```

---

## 📁 Estrutura do Projeto

```
app/
├── auth/               # Lógica de autenticação
│   └── auth_routes.py
├── core/               # Segurança e utilitários
│   └── security.py
├── routes/             # Rotas da API (ex: produtos)
│   └── products.py
├── models.py           # Modelos SQLAlchemy
├── schemas.py          # Pydantic models
├── database.py         # Configuração do banco
├── config.py           # Configurações globais
└── main.py             # Entrada da aplicação
```

---

## 🐘 Banco de Dados

O banco PostgreSQL roda em container, criado via `docker-compose`. A aplicação se conecta automaticamente no startup e cria as tabelas se necessário.

---

## 🧪 Requisitos para rodar localmente (sem Docker)

* Python 3.11+
* PostgreSQL rodando localmente
* Instalar dependências:

```bash
pip install -r requirements.txt
```

---

## 📤 Deploy

Esta aplicação pode ser facilmente publicada em:

* 🚀 [Render](https://render.com)
* 🛫 [Railway](https://railway.app)
* ☁️ VPS com Docker (DigitalOcean, etc.)

---

## 🧑‍💻 Autor

Desenvolvido por [Pedro Cabreira](https://github.com/pcabreira)
Contato: [pclongboard@hotmail.com](mailto:pclongboard@hotmail.com)

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.

````