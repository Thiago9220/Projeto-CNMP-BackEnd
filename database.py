from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados (usando SQLite local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"  # O arquivo do banco de dados será chamado 'database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Cria uma sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa usada para criar os modelos
Base = declarative_base()

# Definindo o modelo de Usuário
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)  # A senha será armazenada com hash
    nome = Column(String)  # Campo nome
    perfil = Column(String)  # Novo campo para o perfil (usuario ou gestor)

# Definindo o modelo de Indicador
class Indicador(Base):
    __tablename__ = "indicadores"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True)
    nome = Column(String, index=True)
    area = Column(String, index=True)
    unidade = Column(String, index=True)
    classificador = Column(String, index=True)
    grupo = Column(String, index=True)
    responsavel = Column(String, index=True)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
