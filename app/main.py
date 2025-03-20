from fastapi import FastAPI
from app.database.db import engine, Base

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API de Monitoramento de Pedidos de Delivery"}

# IMPORTANDO ROTAS

from fastapi import FastAPI
from app.database.db import engine, Base
from app.routes import pedido_routes

app = FastAPI()

# Criando as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Incluindo as rotas de pedidos
app.include_router(pedido_routes.router)

@app.get("/")
def home():
    return {"mensagem": "API de Monitoramento de Pedidos de Delivery"}
