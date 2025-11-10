from connect_to_db import connectToDB, closeConnection

def createTable(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(table)
        print("✅ Tabela criada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")  
    finally:
        cursor.close()

def main():
    conn = connectToDB()
    
    if conn is not None:
        players_table = """
        CREATE TABLE IF NOT EXISTS players (
            player_id VARCHAR(50) PRIMARY KEY,
            matches_played INT DEFAULT 0,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
            draws INT DEFAULT 0
        );  
        """

        matches_table = """
        CREATE TABLE IF NOT EXISTS matches (
            game_id VARCHAR(50) PRIMARY KEY,
            rated BOOLEAN NOT NULL,
            num_turns INT NOT NULL,
            game_status ENUM('mate', 'resign', 'outoftime', 'draw', 'stalemate', 'cheat') NOT NULL,
            winner ENUM('white', 'black', 'draw') NOT NULL,
            
            white_player_id VARCHAR(50),
            white_rating INT,
            black_player_id VARCHAR(50), 
            black_rating INT,
            
            game_duration_seconds BIGINT,

            FOREIGN KEY (white_player_id) REFERENCES players(player_id),
            FOREIGN KEY (black_player_id) REFERENCES players(player_id), 

            INDEX idx_partidas_status (game_status),
            INDEX idx_partidas_vencedor (winner),
            INDEX idx_partidas_brancas (white_player_id),
            INDEX idx_partidas_pretas (black_player_id)
        );
        """

        createTable(conn, players_table)
        createTable(conn, matches_table)
        closeConnection(conn)

if __name__ == "__main__":
    main()
