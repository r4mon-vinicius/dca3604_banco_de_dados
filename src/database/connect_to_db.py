import mysql.connector
import time
import os

def connectToDB():
    """
    Tenta se conectar ao banco de dados MySQL dentro do container Docker.
    Usa o nome do serviço 'db' como host.
    """
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'db'),
                port=os.environ.get('DB_PORT', 3306),
                user=os.environ.get('DB_USER', 'cs'),
                password=os.environ.get('DB_PASSWORD', 'cs123'),
                database=os.environ.get('DB_NAME', 'champsched')
            )
            print("✅ Conexão ao DB (ETL) bem-sucedida.")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Erro ao conectar ao DB: {err}. Tentando novamente... ({retries})")
            retries -= 1
            time.sleep(3)
    
    print("❌ Não foi possível conectar ao banco de dados (ETL).")
    return None

def closeConnection(conn):
    if conn and conn.is_connected():
        conn.close()
        print("✅ Conexão (ETL) encerrada.")