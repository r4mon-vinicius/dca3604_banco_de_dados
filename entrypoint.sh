#!/bin/sh

# Este script garante que o ETL seja executado apenas uma vez.

# 1. CRIA as tabelas (é rápido e usa 'IF NOT EXISTS')
echo "Verificando/Criando tabelas no banco de dados..."
python database/create_db.py

# 2. Verifica se o banco já foi populado.
#    O script python sai com 0 (sucesso) se > 0 linhas, ou 1 (falha) se 0 linhas.
echo "Verificando se o banco de dados está populado..."

if python database/check_if_populated.py; then
    # Exit code 0 (Sucesso): O banco JÁ TEM dados.
    echo "Banco de dados já populado. Pulando ETL."
else
    # Exit code 1 (Falha): O banco está VAZIO.
    echo "Banco de dados vazio. Iniciando ETL pela primeira vez..."
    
    # 2a. Executa o pré-processamento
    echo "Iniciando pré-processamento... (games.csv -> games_clean.csv)"
    python etl/preprocess.py
    
    # 2b. Carga dos dados no banco
    echo "Carregando dados para o MySQL..."
    python etl/load_data.py
    
    echo "Carga do ETL concluída."
fi

# 3. Inicia a aplicação Streamlit
echo "Iniciando aplicação Streamlit..."
streamlit run app.py