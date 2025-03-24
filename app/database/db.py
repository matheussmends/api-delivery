from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define o nome do banco de dados SQLite
DATABASE_URL = "sqlite:///./pedidos.db"  # Caminho para o banco de dados SQLite

# Cria a engine do banco de dados (SQLite)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para as classes do SQLAlchemy
Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()  # Cria a sessão do banco de dados
    try:
        yield db  # Retorna a sessão aberta para ser usada nas rotas
    finally:
        db.close()  # Fecha a sessão após o uso
