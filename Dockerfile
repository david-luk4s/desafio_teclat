# Usar imagem base Python
FROM python:3.11-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .
COPY migrations /app/migrations

# Copiar o script de inicialização e torná-lo executável
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Definir o comando de inicialização
CMD ["/start.sh"]
