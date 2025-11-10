import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.connect_to_db import connectToDB, closeConnection

def loadData(conn, df):

    cursor = conn.cursor()
    try:
        white_players = df[['white_id']].rename(columns={
            'white_id': 'player_id'
        })
        black_players = df[['black_id']].rename(columns={
            'black_id': 'player_id'
        })

        all_players = pd.concat([white_players, black_players]).drop_duplicates().reset_index(drop=True)

        for _, player in all_players.iterrows():
            pid = player['player_id']
            matches_played = ((df['white_id'] == pid) | (df['black_id'] == pid)).sum()

            wins = losses = draws = 0
            if 'winner' in df.columns:
                wins = (
                    ((df['white_id'] == pid) & (df['winner'] == 'white')) |
                    ((df['black_id'] == pid) & (df['winner'] == 'black'))
                ).sum()

                losses = (
                    ((df['white_id'] == pid) & (df['winner'] == 'black')) |
                    ((df['black_id'] == pid) & (df['winner'] == 'white'))
                ).sum()

                draws = (
                    (((df['white_id'] == pid) | (df['black_id'] == pid)) & (df['winner'] == 'draw'))
                ).sum()

            cursor.execute(""" INSERT IGNORE INTO players (
                           player_id, matches_played, wins, losses, draws) VALUES (%s, %s, %s, %s, %s) """, (
                pid,
                int(matches_played),
                int(wins),
                int(losses),
                int(draws)
            ))

        for _, row in df.iterrows():
            cursor.execute(""" INSERT IGNORE INTO matches (
                           game_id, rated, num_turns, game_status, winner,
                           white_player_id, white_rating,
                           black_player_id, black_rating,
                           game_duration_seconds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                row['id'],
                row['rated'],
                row['turns'],
                row['victory_status'],
                row['winner'],
                row['white_id'],
                row['white_rating'],
                row['black_id'],
                row['black_rating'],
                row['game_duration_seconds']
            ))
        conn.commit()

    except Exception as e:
        print(f"Error ao carregar os dados: {e}")
        conn.rollback()
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connectToDB()
    if conn is not None:
        df = pd.read_csv("csv/games_clean.csv")
        loadData(conn, df)
        closeConnection(conn)
