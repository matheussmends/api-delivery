from fastapi import FastAPI
from app.database.db import engine, Base
from app.routes import pedido_routes
from app.models import pedido  # Importação do modelo de pedido

# Criação das tabelas no banco de dados (executa isso uma vez)
Base.metadata.create_all(bind=engine)

# Inicializando a aplicação FastAPI
app = FastAPI()

# Incluindo as rotas de pedidos
app.include_router(pedido_routes.router)

# Rota de exemplo
@app.get("/")
def home():
    return {"mensagem": "API de Monitoramento de Pedidos de Delivery"}
