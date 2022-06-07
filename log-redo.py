import psycopg2
import sys


# Conectando Banco Postgres
def conectandoBanco():
    con = psycopg2.connect(host='localhost',
                            dbname='trabalholog',
                            user='postgres',
                            password='1234')
    #print('conectado')
    return con

# Esecuta comando database sql
def executa_db(sql):
  con = conectandoBanco()
  cur = con.cursor()
  cur.execute(sql)
  con.commit()
  con.close()


# Drop da tabela caso ela ja exista 
sql = 'DROP TABLE IF EXISTS log'
executa_db(sql)

#Criar Tabela log 
sql = 'CREATE TABLE log (id INTEGER, colunaA INTEGER, colunaB INTEGER, valor INTEGER)'
executa_db(sql)

  
""" Abrindo arquivo de log """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        print('Arquivo aberto com sucesso')
        return file
    except:
        print('Erro ao abrir arquivo')


""" Função para imprimir o conteúdo do arquivo """
def printFile(file):
    for line in file:
        print(line)


""" Função que pega o nome do arquivo de entrada"""
def getParam():
    return sys.argv[1]


""" Pega os dados do arquivo e coloca em um vetor """
def getData(file):
    data = []
    for line in file:
        data.append(line)
    return data



""" 
Função que divide os dados em: -Dados para fazer o REDO e - Dados para preencher a tabela
def splitData(data):
    for line in data:
        line = line.split(';')
        return line

    
    FALTA FAZER:

    - Splitar os dados do arquivo em:
        -- Dados de inserção na tabela
        -- Dados do log 
    - Função que percorre o arquivo de dados do log
    - Função que percorre o arquivo de dados de inserção na tabela
    - Funções que o professor pediu para fazer

 """


file = openFile(getParam()) # Abrindo arquivo de log
data = getData(file) # Pegando dados do arquivo e colocando em um vetor






file.close()

