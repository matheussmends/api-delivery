from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.pedido import Pedido
from pydantic import BaseModel
from typing import List
import pandas as pd
from datetime import datetime

# Criando o router
router = APIRouter()

# Modelo de dados para receber pedidos
class PedidoBase(BaseModel):
    id_cliente: int
    valor: float
    status: str = "pendente"
    hora_pedido: datetime = datetime.utcnow()

# Modelo de resposta
class PedidoResponse(PedidoBase):
    id: int

    class Config:
        orm_mode = True

# Criar pedido (POST /pedidos)
@router.post("/pedidos", response_model=PedidoResponse)
def criar_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    try:
        novo_pedido = Pedido(**pedido.dict())
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)
        return novo_pedido
    except Exception as e:
        db.rollback()  # Em caso de erro, desfaz a transação
        raise HTTPException(status_code=500, detail=str(e))

# Listar todos os pedidos (GET /pedidos)
@router.get("/pedidos", response_model=List[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

# Atualizar status do pedido (PUT /pedidos/{id})
class StatusUpdate(BaseModel):
    novo_status: str

@router.put("/pedidos/{id}", response_model=PedidoResponse)
def atualizar_status_pedido(id: int, status: StatusUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = status.novo_status
    db.commit()
    db.refresh(pedido)
    return pedido

# Excluir um pedido (DELETE /pedidos/{id})
@router.delete("/pedidos/{id}")
def deletar_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(pedido)
    db.commit()
    return {"mensagem": f"Pedido {id} excluído com sucesso"}

# Rota para obter estatísticas dos pedidos
@router.get("/estatisticas")
async def obter_estatisticas(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()

    if not pedidos:
        return {"mensagem": "Nenhum pedido cadastrado"}

    # Convertendo os pedidos para um DataFrame do Pandas
    df = pd.DataFrame([{
        "id": p.id,
        "id_cliente": p.id_cliente,
        "valor": p.valor,
        "status": p.status,
        "hora_pedido": p.hora_pedido
    } for p in pedidos])

    # Converter a coluna de data para datetime
    df["hora_pedido"] = pd.to_datetime(df["hora_pedido"])

    # Tempo médio de entrega (diferença entre hora_pedido e pedidos com status "entregue")
    if "entregue" in df["status"].values:
        df_entregues = df[df["status"] == "entregue"]
        tempo_medio_entrega = (df_entregues["hora_pedido"].max() - df_entregues["hora_pedido"].min()).total_seconds() / len(df_entregues)
    else:
        tempo_medio_entrega = None

    # Total de pedidos por status
    pedidos_por_status = df["status"].value_counts().to_dict()

    # Total de pedidos por dia
    pedidos_por_dia = df["hora_pedido"].dt.date.value_counts().to_dict()

    return {
        "tempo_medio_entrega_segundos": tempo_medio_entrega,
        "total_pedidos_por_status": pedidos_por_status,
        "total_pedidos_por_dia": pedidos_por_dia
    }