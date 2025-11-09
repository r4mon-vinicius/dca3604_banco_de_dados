import mysql.connector

def createTable(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(table)
        print("✅ Tabela criada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")  
    finally:
        cursor.close()