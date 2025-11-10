#!/bin/sh

# Este script garante que o ETL seja executado antes do Streamlit iniciar

# 1. Executa o pré-processamento dos dados
echo "Iniciando pré-processamento... (games.csv -> games_clean.csv)"
python3 etl/preprocess.py

# 2. CRIA as tabelas no banco de dados (NOVO PASSO)
echo "Criando tabelas no banco de dados (se não existirem)..."
python3 database/create_db.py

# 3. Carga dos dados no banco de dados
echo "Carregando dados para o MySQL..."
python3 etl/load_data.py

# 4. Inicia a aplicação Streamlit
echo "Iniciando aplicação Streamlit..."
streamlit run app.py