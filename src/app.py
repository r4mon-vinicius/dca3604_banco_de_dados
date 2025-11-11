import streamlit as st
import mysql.connector
import pandas as pd
import time
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_resource(ttl=300) # Adiciona cache para não reconectar a cada interação
def get_connection():
    """
    Tenta se conectar ao banco de dados MySQL dentro do container Docker.
    """
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host="db",
                port=3306,
                user="cs",
                password="cs123",
                database="champsched"
            )
            return conn
        except mysql.connector.Error as err:
            # Isso é útil durante a inicialização do docker-compose
            st.warning(f"Erro ao conectar ao DB: {err}. Tentando novamente... ({retries})")
            retries -= 1
            time.sleep(3)
    
    st.error("Não foi possível conectar ao banco de dados após 10 tentativas.")
    return None

# Adiciona cache para as queries não rodarem a toda hora
@st.cache_data(ttl=600)
def load_data(query, _conn):
    """Executa uma query e retorna um DataFrame."""
    try:
        return pd.read_sql(query, _conn)
    except Exception as e:
        st.error(f"Erro ao executar a query: {e}")
        return pd.DataFrame()

st.title("♘ Dashboard de Análise de Xadrez")

conn = get_connection()

if conn:
    tab_home, tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Sobre",
        "📊 Finais de Jogo",
        "👑 Vantagem das Peças",
        "🕒 Duração das Partidas (Turnos)",
        "🏆 Top 10 Jogadores"
    ])

    with tab_home:
        st.header("Sobre este Projeto")
        
        st.subheader("Visão Geral dos Dados")
        
        # Queries para contar os dados
        query_matches = "SELECT COUNT(*) as total FROM matches"
        query_players = "SELECT COUNT(*) as total FROM players"
        
        # Carrega os dados
        df_total_matches = load_data(query_matches, conn)
        df_total_players = load_data(query_players, conn)
        
        # Garante que os dados foram carregados
        if not df_total_matches.empty and not df_total_players.empty:
            # Extrai o número do dataframe (iloc[0] pega a primeira linha)
            total_matches = int(df_total_matches['total'].iloc[0])
            total_players = int(df_total_players['total'].iloc[0])
            
            # Usa colunas para exibir as métricas lado a lado
            col1, col2 = st.columns(2)
            
            # Formata o número (ex: 10000 -> 10.000)
            col1.metric("Total de Partidas Registradas", f"{total_matches:,.0f}".replace(",", "."))
            col2.metric("Total de Jogadores Únicos", f"{total_players:,.0f}".replace(",", "."))
        else:
            st.warning("Ainda não há dados para exibir as métricas.")
        
        st.divider() # Adiciona uma linha divisória
        st.markdown("""
            Este dashboard foi criado para analisar dados de partidas de xadrez
            armazenadas em um banco de dados MySQL. Todas as análises são feitas
            diretamente a partir dos dados contidos no banco, também são exibidas todos os 
            comandos SQL utilizados para extrair os insights.
            
            Os dados estão divididos em duas tabelas principais:
            * `matches`: Contém informações detalhadas sobre cada partida.
            * `players`: Contém estatísticas agregadas sobre cada jogador.
            
            Use as abas acima para explorar os diferentes insights sobre os dados.
        """)

    with tab1:
        st.header("Como as Partidas Terminam?")
        query = "SELECT game_status, COUNT(*) as total FROM matches GROUP BY game_status ORDER BY total DESC"
        df_status = load_data(query, conn)
        st.markdown(f"```sql\n{query}\n```")
        
        if not df_status.empty:
            traducoes_status = {
                'mate': 'Xeque-mate',
                'resign': 'Abandono',
                'outoftime': 'Tempo Esgotado',
                'draw': 'Empate (Acordo)',
                'stalemate': 'Rei Afogado (Empate)',
                'cheat': 'Trapaça'
            }
            df_status['status_traduzido'] = df_status['game_status'].map(traducoes_status).fillna(df_status['game_status'])
            
            st.bar_chart(df_status, x='status_traduzido', y='total', sort=False)
        else:
            st.warning("Não há dados na tabela 'matches' para exibir.")

    with tab2:
        st.header("Vantagem: Brancas vs. Pretas")
        query = "SELECT winner, COUNT(*) as total FROM matches WHERE winner IN ('white', 'black', 'draw') GROUP BY winner"
        df_winner = load_data(query, conn)
        st.markdown(f"```sql\n{query}\n```")
        
        if not df_winner.empty:
            traducoes_cores = {
                'white': 'Vitórias das Brancas',
                'black': 'Vitórias das Pretas',
                'draw': 'Empates'
            }

            df_winner['winner_traduzido'] = df_winner['winner'].map(traducoes_cores).fillna(df_winner['winner'])

            # Define um tamanho de figura razoável
            fig, ax = plt.subplots(figsize=(7, 5))
            
            # Cores para W/B/D
            colors = ['#FFFFFF', "#1D1D1D", "#747474"]
            
            ax.pie(
                df_winner['total'],
                labels=df_winner['winner_traduzido'].astype(str).tolist(),
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                wedgeprops={'edgecolor': 'black'}
            )
            ax.axis('equal')
            
            col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
            
            # Coloca o gráfico na coluna central (col2)
            with col2:
                st.pyplot(fig)
        else:
            st.warning("Não há dados na tabela 'matches' para exibir.")

    with tab3:
        st.header("Distribuição da Duração das Partidas (em turnos)")
        query = "SELECT num_turns FROM matches WHERE num_turns > 0 AND num_turns <= 150"
        df_turns = load_data(query, conn)
        st.markdown(f"```sql\n{query}\n```")
        
        if not df_turns.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df_turns['num_turns'], bins=30, edgecolor='black', alpha=0.7)
            ax.set_title('Distribuição do Número de Turnos por Partida')
            ax.set_xlabel('Número de Turnos')
            ax.set_ylabel('Frequência (Nº de Partidas)')
            
            col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

            with col2:
                st.pyplot(fig) # Não precisa de 'use_container_width'
        else:
            st.warning("Não há dados na tabela 'matches' para exibir.")

    with tab4:
        st.header("Top 10 Jogadores por Vitórias")
        query = "SELECT player_id, wins FROM players ORDER BY wins DESC LIMIT 10"
        df_players = load_data(query, conn)
        st.markdown(f"```sql\n{query}\n```")
        
        if not df_players.empty:
            st.bar_chart(df_players, x='player_id', y='wins', sort=False)
        else:
            st.warning("Não há dados na tabela 'players' para exibir.")

    # Fecha a conexão após carregar todos os dados
    conn.close()
else:
    st.error("Falha na conexão com o banco de dados. Verifique os logs do container.")