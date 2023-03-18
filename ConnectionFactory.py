import pyodbc

# Essa classe estabelecerá a conexão com o banco de dados
def get_connection(server, database):
    connection_data = (
                        "Driver={SQL Server Native Client 11.0};"
                        f"Server={server};"
                        f"Database={database};"
                        "Trusted_Connection=yes;"
                        )
    conn = pyodbc.connect(connection_data)
    return conn

# Caso estejamos executando essa classe, o algoritmo a seguir irá testar o método 'get_connection()'
if __name__ == '__main__':
    conn = get_connection("localhost\SQLEXPRESS", "ImagineCup")
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM Produto').fetchall():
        for column in row:
            print(column)
    conn.close()