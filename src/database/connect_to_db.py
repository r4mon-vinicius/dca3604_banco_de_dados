import mysql.connector

def connectToDB():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='cs',
            password='cs123',
            database='champsched'
        )
        return connection
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return None
    
def closeConnection(conn):
    if conn.is_connected():
        conn.close()
        print("✅ Conexão encerrada.")
    else:
        print("❌ Erro: Conexão não está aberta.")