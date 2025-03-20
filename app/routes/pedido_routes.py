from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.pedido import Pedido
from datetime import datetime
from pydantic import BaseModel
from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.database.db import get_db
from app.models.pedido import Pedido

# Criando o router
router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    novo_pedido = Pedido(**pedido.dict())
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

# Listar todos os pedidos (GET /pedidos)
@router.get("/pedidos", response_model=List[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

# Atualizar status do pedido (PUT /pedidos/{id})

from fastapi import HTTPException

@router.put("/pedidos/{id}", response_model=PedidoResponse)
def atualizar_status_pedido(id: int, novo_status: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")  # Corrigido!

    pedido.status = novo_status
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

    return {"mensagem": "Pedido excluído com sucesso"}

# CRIANDO A ROTA DE ESTATISTICAS
router = APIRouter()

# Rota para obter estatísticas dos pedidos
@router.get("/estatisticas")
def obter_estatisticas(db: Session = Depends(get_db)):
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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.pedido import Pedido
from pydantic import BaseModel

# Define a nova classe de dados para o corpo da requisição
# A classe Pydantic é usada para receber o status a ser atualizado na requisição. Ela tem um único campo, novo_status, que será passado no corpo da requisição.
class StatusUpdate(BaseModel):
    novo_status: str

router = APIRouter()

# Rota para atualizar o status de um pedido
# A função atualizar_status_pedido recebe o ID do pedido a ser atualizado e o novo status. Primeiro, ela verifica se o pedido existe no banco de dados. Caso contrário, retorna um erro 404 com a mensagem "Pedido não encontrado". Caso o pedido seja encontrado, o status é atualizado, as mudanças são salvas no banco de dados e o pedido atualizado é retornado.
@router.put("/pedidos/{id}")
def atualizar_status_pedido(id: int, status: StatusUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = status.novo_status
    db.commit()
    db.refresh(pedido)
    return {"mensagem": f"Status do pedido {id} atualizado para {pedido.status}"}

# EXCLUIR PEDIDO

# A função excluir_pedido recebe o ID do pedido a ser excluído. Primeiro, ela verifica se o pedido existe no banco de dados. Caso contrário, retorna um erro 404 com a mensagem "Pedido não encontrado". Se o pedido for encontrado, ele é deletado, as mudanças são salvas no banco de dados e uma mensagem de sucesso é retornada.
@router.delete("/pedidos/{id}")
def excluir_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(pedido)
    db.commit()
    return {"mensagem": f"Pedido {id} excluído com sucesso"}

# OBTER ROTA DA ESTATÍSTICA DE PEDIDOS

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.pedido import Pedido
import pandas as pd
from datetime import datetime

router = APIRouter()

@router.get("/estatisticas")
async def get_estatisticas(db: Session = Depends(get_db)):
    try:
        # Obtém todos os pedidos
        pedidos = db.query(Pedido).all()

        # Cria um DataFrame a partir dos pedidos
        df = pd.DataFrame([pedido.__dict__ for pedido in pedidos])

        # Converte a coluna 'hora_pedido' para datetime
        df['hora_pedido'] = pd.to_datetime(df['hora_pedido'], errors='coerce')

        # Verifica se a coluna 'hora_entrega' existe no DataFrame
        if 'hora_entrega' in df.columns:
            # Converte a coluna 'hora_entrega' para datetime, com tratamento de erros
            df['hora_entrega'] = pd.to_datetime(df['hora_entrega'], errors='coerce')

            # Exibe as colunas convertidas para depuração
            print("DataFrame após conversão de horas:")
            print(df[['hora_pedido', 'hora_entrega']])

            # Filtra apenas os pedidos com status 'entregue'
            pedidos_entregues = df[df['status'] == 'entregue']

            if not pedidos_entregues.empty:
                # Calcula o tempo de entrega (diferença entre hora_entrega e hora_pedido)
                pedidos_entregues['tempo_entrega'] = (pedidos_entregues['hora_entrega'] - pedidos_entregues['hora_pedido']).dt.total_seconds() / 3600

                # Exibe os tempos de entrega calculados para depuração
                print("Tempos de entrega calculados:")
                print(pedidos_entregues['tempo_entrega'])

                # Calcula o tempo médio de entrega
                tempo_medio_entrega = pedidos_entregues['tempo_entrega'].mean()
                if pd.isna(tempo_medio_entrega):  # Se o valor for NaN
                    tempo_medio_entrega = 0  # Define o tempo médio como 0 se não houver entregas válidas
            else:
                tempo_medio_entrega = 0  # Nenhum pedido entregue
        else:
            tempo_medio_entrega = 0  # Caso não haja coluna 'hora_entrega'

        # Estatísticas adicionais
        total_pedidos_por_status = df['status'].value_counts().to_dict()
        total_pedidos_por_dia = df['hora_pedido'].dt.date.value_counts().to_dict()

        return {
            "tempo_medio_entrega": tempo_medio_entrega,
            "total_pedidos_por_status": total_pedidos_por_status,
            "total_pedidos_por_dia": total_pedidos_por_dia
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))