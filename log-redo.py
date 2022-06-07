import psycopg2

#Conectando Banco Postgres
def conectandoBanco():
    con = psycopg2.connect(host='localhost',
                            dbname='trabalholog',
                            user='postgres',
                            password='1234')
    #print('conectado')
    return con

def criar_db(sql):
  con = conectandoBanco()
  cur = con.cursor()
  cur.execute(sql)
  con.commit()
  con.close()

  
""" Abrindo arquivo de log """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        print('Arquivo aberto com sucesso')
        return file
    except:
        print('Erro ao abrir arquivo')



file = openFile('entrada1.txt')

