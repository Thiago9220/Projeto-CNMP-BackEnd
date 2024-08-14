from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./indicadores.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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



# Modelo Pydantic para leitura de Indicadores (usado nas respostas)
class IndicadorRead(BaseModel):
    id: int
    codigo: str
    nome: str
    area: str
    unidade: str
    classificador: str
    grupo: str
    responsavel: str

    class Config:
        orm_mode = True

