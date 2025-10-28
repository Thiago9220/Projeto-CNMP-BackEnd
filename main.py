import os
import shutil
import bcrypt
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database

app = FastAPI()

uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UsuarioCreate(BaseModel):
    email: str
    senha: str
    nome: str
    perfil: str


class UsuarioRead(BaseModel):
    id: int
    email: str
    nome: str
    perfil: str
    foto_perfil: str = None

    class Config:
        orm_mode = True


@app.post("/usuarios/", response_model=UsuarioRead)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(database.Usuario).filter(database.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email jǭ cadastrado")

    hashed_senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())

    novo_usuario = database.Usuario(
        email=usuario.email,
        senha=hashed_senha.decode("utf-8"),
        nome=usuario.nome,
        perfil=usuario.perfil,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


class UsuarioLogin(BaseModel):
    email: str
    senha: str


@app.post("/login/")
def login_usuario(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(database.Usuario).filter(database.Usuario.email == usuario.email).first()
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Usuǭrio nǜo encontrado")

    if not bcrypt.checkpw(usuario.senha.encode("utf-8"), db_usuario.senha.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Senha incorreta")

    return {
        "access_token": "seuTokenDeAutenticacao",
        "token_type": "bearer",
        "nome": db_usuario.nome,
        "perfil": db_usuario.perfil,
        "usuario_id": db_usuario.id,
    }


@app.get("/usuarios/", response_model=list[UsuarioRead])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(database.Usuario).all()


class IndicadorCreate(BaseModel):
    codigoIndicador: str
    nomeIndicador: str
    objetivoEstrategico: str
    perspectivaEstrategica: str
    descricaoObjetivoEstrategico: str
    descricaoIndicador: str
    finalidadeIndicador: str
    dimensaoDesempenho: str
    formula: str
    fonteFormaColeta: str
    pesoIndicador: str
    interpretacaoIndicador: str
    areaResponsavel: str
    meta: str
    tiposAcumulacao: str
    polaridade: str
    periodicidadeColeta: str
    frequenciaMeta: str
    unidadeMedida: str


class IndicadorRead(IndicadorCreate):
    id: int

    class Config:
        orm_mode = True


@app.post("/indicadores/", response_model=IndicadorRead)
def create_indicador(indicador: IndicadorCreate, db: Session = Depends(get_db)):
    db_indicador = database.Indicador(**indicador.dict())
    db.add(db_indicador)
    db.commit()
    db.refresh(db_indicador)
    return db_indicador


@app.get("/indicadores/", response_model=list[IndicadorRead])
def get_indicadores(db: Session = Depends(get_db)):
    return db.query(database.Indicador).all()


@app.put("/usuarios/{usuario_id}/atualizar_perfil", response_model=UsuarioRead)
async def atualizar_perfil(
    usuario_id: int,
    nome: str = Form(...),
    senha_antiga: str = Form(...),
    nova_senha: str = Form(...),
    foto_perfil: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    usuario = db.query(database.Usuario).filter(database.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuǭrio nǜo encontrado")

    if not bcrypt.checkpw(senha_antiga.encode("utf-8"), usuario.senha.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta")

    usuario.nome = nome
    hashed_senha = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt())
    usuario.senha = hashed_senha.decode("utf-8")

    if foto_perfil:
        upload_dir = "uploads/perfis"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = os.path.splitext(foto_perfil.filename)[1]
        file_location = f"{upload_dir}/{usuario_id}{file_extension}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(foto_perfil.file, buffer)

        usuario.foto_perfil = file_location

    db.commit()
    db.refresh(usuario)
    return usuario
