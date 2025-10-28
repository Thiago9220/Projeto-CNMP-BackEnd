from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    nome = Column(String)
    perfil = Column(String)
    foto_perfil = Column(String, nullable=True)


class Indicador(Base):
    __tablename__ = "indicadores"

    id = Column(Integer, primary_key=True, index=True)
    codigoIndicador = Column(String)
    nomeIndicador = Column(String)
    objetivoEstrategico = Column(String)
    perspectivaEstrategica = Column(String)
    descricaoObjetivoEstrategico = Column(String)
    descricaoIndicador = Column(String)
    finalidadeIndicador = Column(String)
    dimensaoDesempenho = Column(String)
    formula = Column(String)
    fonteFormaColeta = Column(String)
    pesoIndicador = Column(String)
    interpretacaoIndicador = Column(String)
    areaResponsavel = Column(String)
    meta = Column(String)
    tiposAcumulacao = Column(String)
    polaridade = Column(String)
    periodicidadeColeta = Column(String)
    frequenciaMeta = Column(String)
    unidadeMedida = Column(String)


Base.metadata.create_all(bind=engine)
