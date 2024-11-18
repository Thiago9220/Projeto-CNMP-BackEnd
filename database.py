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
    foto_perfil = Column(String, nullable=True)
    

# Definindo o modelo de Indicador
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

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
