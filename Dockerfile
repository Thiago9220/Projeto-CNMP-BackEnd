# Usar a imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos e instalar dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte do projeto
COPY . .

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
