import pandas as pd

def preprocessData(df):
    df_clean = df.copy()

    df_clean = df_clean.dropna()
    df_clean = df_clean.drop_duplicates()

    df_clean['rated'] = df_clean['rated'].map({'TRUE': True, 'FALSE': False, True: True, False: False})
    df_clean['created_at'] = pd.to_numeric(df_clean['created_at'], errors='coerce')
    df_clean['last_move_at'] = pd.to_numeric(df_clean['last_move_at'], errors='coerce')
    df_clean['turns'] = pd.to_numeric(df_clean['turns'], errors='coerce').fillna(0).astype(int)
    df_clean['white_rating'] = pd.to_numeric(df_clean['white_rating'], errors='coerce').fillna(1200).astype(int)
    df_clean['black_rating'] = pd.to_numeric(df_clean['black_rating'], errors='coerce').fillna(1200).astype(int)
    df_clean['opening_ply'] = pd.to_numeric(df_clean['opening_ply'], errors='coerce').fillna(0).astype(int)

    df_clean['victory_status'] = df_clean['victory_status'].str.strip().str.lower()
    df_clean['winner'] = df_clean['winner'].str.strip().str.lower()
    df_clean['opening_eco'] = df_clean['opening_eco'].str.strip().str.upper()
    
    df_clean['game_duration_seconds'] = (df_clean['last_move_at'] - df_clean['created_at']) / 1000

    return df_clean


if __name__ == "__main__":
    df = pd.read_csv("csv/games.csv")
    df_clean = preprocessData(df)
    df_clean.to_csv("csv/games_clean.csv", index=False)