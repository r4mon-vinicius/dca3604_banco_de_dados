# 🏆 Dashboard de Análise de Partidas de Xadrez

Este repositório contém o código para um pipeline de dados e um dashboard de visualização focado em um [dataset de partidas de xadrez do Kaggle](https://www.kaggle.com/datasets/datasnaek/chess).

O projeto utiliza **Docker Compose** para orquestrar um banco de dados **MySQL** e uma aplicação **Streamlit**. Ao iniciar, um processo de ETL (Extração, Transformação e Carga) é executado automaticamente: os dados do CSV são limpos, processados com Pandas e carregados no banco de dados MySQL. Após a carga, o dashboard é iniciado e exibe insights sobre os dados.

## ✨ Funcionalidades do Dashboard

O dashboard interativo é dividido em várias seções, cada uma extraindo dados do MySQL em tempo real:

  * **Visão Geral:** Métricas principais com o número total de partidas e jogadores únicos.
  * **Finais de Jogo:** Gráfico de barras mostrando a distribuição de como as partidas terminaram (xeque-mate, abandono, tempo, etc.).
  * **Vantagem das Peças:** Gráfico de pizza que compara a taxa de vitórias das peças brancas, pretas e empates.
  * **Duração das Partidas:** Histograma com a distribuição do número de turnos por partida.
  * **Top 10 Jogadores:** Gráfico de barras com os 10 jogadores com maior número de vitórias.

## 🛠️ Tecnologias Utilizadas

  * **Visualização:** Streamlit
  * **Banco de Dados:** MySQL 8.0
  * **Processamento de Dados (ETL):** Python, Pandas
  * **Orquestração/Containerização:** Docker e Docker Compose

## 🚀 Como Executar o Projeto

### Pré-requisitos

  * [Docker](https://docs.docker.com/engine/install/)
  * [Docker Compose](https://docs.docker.com/compose/install/)
  * O arquivo `games.csv` do [dataset do Kaggle](https://www.kaggle.com/datasets/datasnaek/chess).

### Passos de Instalação

1.  **Clone o repositório:**

    HTTPS:
    ```bash
    git clone https://github.com/r4mon-vinicius/dca3604_banco_de_dados
    ```

    SSH:
    ```bash
    git clone git@github.com:r4mon-vinicius/dca3604_banco_de_dados.git
    ```

2.  **Adicione os dados:**
    Coloque o arquivo `games.csv` que você baixou do Kaggle dentro da pasta `./csv/` na raiz do projeto.

3.  **Construa e inicie os contêineres:**
    Na raiz do projeto, execute o comando:

    ```bash
    docker compose up --build
    ```

4.  **Aguarde o ETL:**
    Ao iniciar pela primeira vez, o contêiner `champsched-app` irá executar os scripts de pré-processamento e carregar todos os dados no banco de dados. Você verá logs como `Iniciando pré-processamento...` e `Carregando dados para o MySQL...` no seu terminal.

    **Este processo pode demorar alguns minutos.**

5.  **Acesse o Dashboard:**
    Após o término do ETL, o servidor Streamlit será iniciado. Você pode acessar o dashboard no seu navegador no endereço:

    [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501)

-----