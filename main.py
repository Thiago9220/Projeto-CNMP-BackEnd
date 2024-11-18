import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import database
import bcrypt
import shutil

# Criação do aplicativo FastAPI
app = FastAPI()

uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite acesso apenas do frontend local
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Monta o diretório de uploads para servir arquivos estáticos
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Criar as tabelas no banco de dados
database.Base.metadata.create_all(bind=database.engine)

# Dependência para obter a sessão de banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo Pydantic para criação de usuário
class UsuarioCreate(BaseModel):
    email: str
    senha: str
    nome: str
    perfil: str  # Adicionar o campo perfil

# Modelo Pydantic para retorno de informações do usuário
class UsuarioRead(BaseModel):
    id: int
    email: str
    nome: str
    perfil: str
    foto_perfil: str = None  # Novo campo

    class Config:
        orm_mode = True

# Endpoint para adicionar um novo usuário (com hash de senha)
@app.post("/usuarios/", response_model=UsuarioRead)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se o email já existe no banco de dados
    db_usuario = db.query(database.Usuario).filter(database.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria o hash da senha
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
    
    # Cria o novo usuário com a senha hash e o perfil
    novo_usuario = database.Usuario(
        email=usuario.email, 
        senha=hashed_senha.decode('utf-8'), 
        nome=usuario.nome,
        perfil=usuario.perfil  # Adicionar o perfil ao usuário
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# Modelo Pydantic para login de usuário
class UsuarioLogin(BaseModel):
    email: str
    senha: str

# Endpoint para login
@app.post("/login/")
def login_usuario(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    db_usuario = db.query(database.Usuario).filter(database.Usuario.email == usuario.email).first()
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    
    # Verifica se a senha está correta
    if not bcrypt.checkpw(usuario.senha.encode('utf-8'), db_usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Senha incorreta")
    
    # Retorna o token de acesso fictício (você pode melhorar isso para um token JWT real)
    return {
        "access_token": "seuTokenDeAutenticacao", 
        "token_type": "bearer", 
        "nome": db_usuario.nome,
        "perfil": db_usuario.perfil,
        "usuario_id": db_usuario.id  # Retornar o ID do usuário
    }

# Endpoint para obter a lista de usuários (opcional para debug)
@app.get("/usuarios/", response_model=list[UsuarioRead])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(database.Usuario).all()

# Modelo Pydantic para criação de Indicadores
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

# Modelo Pydantic para leitura de Indicadores (usado nas respostas)
class IndicadorRead(IndicadorCreate):
    id: int

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

# Endpoint para atualizar o perfil do usuário
@app.put("/usuarios/{usuario_id}/atualizar_perfil", response_model=UsuarioRead)
async def atualizar_perfil(
    usuario_id: int,
    nome: str = Form(...),
    senha_antiga: str = Form(...),
    nova_senha: str = Form(...),
    foto_perfil: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    usuario = db.query(database.Usuario).filter(database.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verifica se a senha antiga está correta
    if not bcrypt.checkpw(senha_antiga.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta")

    # Atualiza o nome e a nova senha
    usuario.nome = nome
    hashed_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
    usuario.senha = hashed_senha.decode('utf-8')

    # Lida com o upload da foto de perfil
    if foto_perfil:
        # Define o caminho para salvar a imagem
        upload_dir = "uploads/perfis"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = os.path.splitext(foto_perfil.filename)[1]
        file_location = f"{upload_dir}/{usuario_id}{file_extension}"
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(foto_perfil.file, buffer)
        
        # Atualiza o campo foto_perfil com o caminho do arquivo
        usuario.foto_perfil = file_location

    db.commit()
    db.refresh(usuario)
    return usuario
