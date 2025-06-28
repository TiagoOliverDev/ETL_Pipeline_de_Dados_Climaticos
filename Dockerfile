# Use imagem oficial do Python
FROM python:3.11-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    # build-essential e libpq-dev são necessários para compilar o psycopg2 (driver do Postgres)
    build-essential \
    libpq-dev \
    # Limpa o cache do apt para manter a imagem final menor
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Otimização de Cache: Copiar e Instalar Dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o Código da Aplicação
COPY . .

# Comando para rodar o pipeline
CMD ["python", "main.py"]
