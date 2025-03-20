from sqlalchemy import create_engine
# create_engine() cria a conexão com o banco SQLite
from sqlalchemy.orm import sessionmaker, declarative_base

# Define o nome do banco de dados SQLite
DATABASE_URL = "sqlite:///./pedidos.db"

# Cria a engine do banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Cria a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base para as classes do SQLAlchemy
# Base usado para criar os modelos do banco
Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()