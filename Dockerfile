# Use uma imagem oficial do Python como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo do diretório atual para o diretório de trabalho dentro do container
COPY . .

# Define a variável de ambiente para garantir que as mensagens de log da aplicação 
# sejam exibidas no console (útil para depuração)
ENV PYTHONUNBUFFERED=1

# Comando para executar a aplicação
CMD ["python", "run.py"]
