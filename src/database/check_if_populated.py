import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connect_to_db import connectToDB

def check_population():
    """
    Verifica se o banco de dados já foi populado.
    - Sai com código 0 se estiver populado (Sucesso para o shell)
    - Sai com código 1 se estiver vazio (Falha para o shell)
    """
    conn = connectToDB()
    if conn is None:
        print("❌ Falha ao conectar ao DB para checagem.")
        sys.exit(1) # Falha (considera vazio)

    try:
        cursor = conn.cursor()
        # Verifica a tabela 'matches', que é a principal
        cursor.execute("SELECT COUNT(*) FROM matches")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Banco de dados já populado. ({count} partidas encontradas)")
            sys.exit(0) # Sucesso (significa "populado")
        else:
            print("⚠️ Banco de dados vazio. (0 partidas)")
            sys.exit(1) # Falha (significa "vazio")
    except Exception as e:
        # Se a tabela não existir (erro 1146), também considera vazio
        print(f"⚠️ Banco de dados vazio ou erro: {e}")
        sys.exit(1) # Falha (significa "vazio")
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    check_population()