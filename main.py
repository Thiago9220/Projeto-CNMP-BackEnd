from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir acesso apenas do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.get("/indicadores/")
def get_indicadores():
    indicadores = [
        {"id": 89, "codigo": "BIBLIO I.1", "nome": "Quantidade de Empréstimos", "area": "BIBLIO Biblioteca", "unidade": "Qtd.", "classificador": "Monitoramento Operacional", "grupo": "-", "responsavel": "Igor Guevara"},
        {"id": 90, "codigo": "BIBLIO I.2", "nome": "Quantidade de Demanda Reprimida", "area": "BIBLIO Biblioteca", "unidade": "Qtd.", "classificador": "Monitoramento Operacional", "grupo": "-", "responsavel": "Sávio Neves do Nascimento"},
        # Adicione mais indicadores aqui
    ]
    return indicadores
