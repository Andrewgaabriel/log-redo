from cmath import log
import psycopg2
import sys


""" Faz a conexão com o Banco de Dados """
def conectandoBanco():
    con = psycopg2.connect( host='localhost',
                            dbname='trabalholog',
                            user='postgres',
                            password='1234')
    return con



""" Executa algum comando SQL no banco de dados """
def executa_db(sql):
    con = conectandoBanco()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        con.rollback()
        con.close()
        return 1
    cur.close()

# Drop da tabela caso ela ja exista 
sql = 'DROP TABLE IF EXISTS log'
executa_db(sql)

#Criar Tabela log 
sql = 'CREATE TABLE log'
executa_db(sql)


# Inserindo Registro
def insereBanco( id, A, B ):
    sql = """ INSERT INTO log (id, colunaA, colunaB) VALUES ('%d','%d','%d'); """ % (id, A, B)
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

