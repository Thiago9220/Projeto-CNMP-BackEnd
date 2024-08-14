from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import database

# Criação do aplicativo FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite acesso apenas do frontend local
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Criar as tabelas no banco de dados
database.Base.metadata.create_all(bind=database.engine)

# Dependência para obter a sessão de banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo Pydantic para validação de dados ao criar um novo indicador
class IndicadorCreate(BaseModel):
    codigo: str
    nome: str
    area: str
    unidade: str
    classificador: str
    grupo: str
    responsavel: str

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

# Endpoint para adicionar um novo indicador ao banco de dados
@app.post("/indicadores/", response_model=IndicadorRead)
def create_indicador(indicador: IndicadorCreate, db: Session = Depends(get_db)):
    db_indicador = database.Indicador(**indicador.dict())
    db.add(db_indicador)
    db.commit()
    db.refresh(db_indicador)
    return db_indicador

# Endpoint para obter a lista de indicadores do banco de dados
@app.get("/indicadores/", response_model=list[IndicadorRead])
def get_indicadores(db: Session = Depends(get_db)):
    indicadores = db.query(database.Indicador).all()
    return indicadores
