# Use a imagem Python 3.9 slim
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do backend
COPY . .

# Exponha a porta 8000 para o FastAPI
EXPOSE 8000

# Comando para iniciar o backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
