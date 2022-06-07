import psycopg2

#Conectando Banco Postgres
def conectandoBanco():
    conn = psycopg2.connect(
    host='localhost'
    dbname='TrabalhoLog'
    user='postgres'
    password='1234'
    )
    print('conectado') #para teste
    return conn

def conecta(con, sql):
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def openFile {

    print("Opening file...")
    file = open("nome-do-arquivo", "r")
    print("File opened.")
    return file
}
