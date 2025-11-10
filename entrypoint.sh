#!/bin/sh

# Este script garante que o ETL seja executado antes do Streamlit iniciar

# 1. Executa o pré-processamento dos dados
echo "Iniciando pré-processamento... (games.csv -> games_clean.csv)"
python etl/preprocess.py

# 2. Carga dos dados no banco de dados
echo "Carregando dados para o MySQL..."
python etl/load_data.py

# 3. Inicia a aplicação Streamlit
echo "Iniciando aplicação Streamlit..."
streamlit run app.py