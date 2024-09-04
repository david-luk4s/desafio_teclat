#!/bin/sh

# Espera o banco de dados PostgreSQL iniciar
echo "Aguardando o banco de dados iniciar..."
sleep 5  # Aguarda 5 segundos para garantir que o banco de dados esteja disponível

# Verifica se o diretório de migrações existe e aplica as migrações
if [ -d "/app/migrations" ]; then
    echo "Aplicando migrações do banco de dados..."
    flask db migrate -m "Initial migration."
    flask db upgrade
else
    echo "Diretório de migrações não encontrado. Por favor, execute 'flask db init' para criar o diretório."
    exit 1
fi

# Inicia o servidor Flask
echo "Iniciando o servidor Flask..."
flask run --host=0.0.0.0
