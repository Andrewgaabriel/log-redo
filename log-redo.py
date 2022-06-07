import psycopg2



""" Conectando ao banco de dados """
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


""" Abrindo arquivo de log """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        print('Arquivo aberto com sucesso')
        return file
    except:
        print('Erro ao abrir arquivo')



file = openFile('entrada1.txt')

