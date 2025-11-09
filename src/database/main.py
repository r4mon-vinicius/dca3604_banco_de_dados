import mysql.connector
from connect_to_db import connectToDB, closeConnection
from create_tables import createTable

def main():
    conn = connectToDB()
    
    if conn is not None:
        players_table = """
        CREATE TABLE IF NOT EXISTS players (
            player_id VARCHAR(50) PRIMARY KEY,
            rating INT DEFAULT 1200,
            matches_played INT DEFAULT 0,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
            draws INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );  
        """

        openings_table = """
        CREATE TABLE IF NOT EXISTS openings (
            eco_code VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            variation VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        matches_table = """
        CREATE TABLE IF NOT EXISTS matches (
            game_id VARCHAR(50) PRIMARY KEY,
            rated BOOLEAN NOT NULL,
            start_time BIGINT,
            end_time BIGINT,
            num_turns INT NOT NULL,
            game_status ENUM('mate', 'resign', 'outoftime', 'draw', 'stalemate', 'cheat') NOT NULL,
            winner ENUM('white', 'black', 'draw') NOT NULL,
            time_increment VARCHAR(20),
            
            -- Referências aos jogadores
            white_player_id VARCHAR(50),
            white_rating INT,
            black_player_id VARCHAR(50), 
            black_rating INT,

            all_moves TEXT,
            opening_eco VARCHAR(10),
            opening_name VARCHAR(255),
            opening_ply INT,
            
            -- Campos calculados
            rating_change_white INT DEFAULT 0,
            rating_change_black INT DEFAULT 0,
            game_duration_seconds BIGINT,
            
            -- Timestamps
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (white_player_id) REFERENCES players(player_id),
            FOREIGN KEY (black_player_id) REFERENCES players(player_id), 
            FOREIGN KEY (opening_eco) REFERENCES openings(eco_code),

            INDEX idx_partidas_tempo (start_time),
            INDEX idx_partidas_status (game_status),
            INDEX idx_partidas_vencedor (winner),
            INDEX idx_partidas_abertura (opening_eco),
            INDEX idx_partidas_brancas (white_player_id),
            INDEX idx_partidas_pretas (black_player_id)
        );
        """

        createTable(conn, players_table)
        createTable(conn, openings_table)
        createTable(conn, matches_table)
        closeConnection(conn)

if __name__ == "__main__":
    main()
