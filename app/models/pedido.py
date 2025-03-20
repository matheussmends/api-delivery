from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.db import Base

class Pedido(Base):
    __tablename__ = "pedidos"

# id -- identificador unico do pedido
    id = Column(Integer, primary_key=True, index=True)
# id_cliente -- o cliente que fez o pedido
    id_cliente = Column(Integer, nullable=False)
# valor -- valor total do pedido
    valor = Column(Float, nullable=False)
# status -- status do pedido
    status = Column(String, default="pendente")
# hora_pedido -- data e horario do pedido
    hora_pedido = Column(DateTime, default=datetime.utcnow)
