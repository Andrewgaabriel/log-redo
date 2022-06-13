from cmath import log
import psycopg2
import sys


""" --------------------Estrutura de dados para armazenar as tuplas---------------------------- """
class Linha:

    def init(self):
        self.id = 0
        self.colunaA = ''
        self.colunaB = ''

    def setId(self, id):
        self.id = id

    def setColunaA(self, colunaA):
        self.colunaA = colunaA

    def setColunaB(self, colunaB):
        self.colunaB = colunaB

""" -------------------------------------------------------------------------------------------- """


""" ------------------Faz a conexão com o Banco de Dados---------------------------------------- """
def conectandoBanco():
    con = psycopg2.connect( host='localhost',
                            dbname='trabalholog',
                            user='postgres',
                            password='postgres')
    return con

""" -------------------------------------------------------------------------------------------- """



""" -------------------Executa algum comando SQL no banco de dados-------------------------------- """
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

""" -------------------------------------------------------------------------------------------- """



""" --------------Inserindo Registro------------------------------------------------------------- """

def insereBanco( id, A, B):
    sql = """ INSERT INTO log (id, colunaA, colunaB) VALUES ('%d','%d','%d'); """ % (id, A, B)
    executa_db(sql)
""" -------------------------------------------------------------------------------------------- """



""" -----------------Abrindo arquivo de log------------------------------------------------------- """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        print('Arquivo aberto com sucesso')
        return file
    except:
        print('Erro ao abrir arquivo')

""" -------------------------------------------------------------------------------------------- """



""" -----------------------Função para imprimir conteúdo---------------------------------------- """
def printFile(file):
    for line in file:
        print(line)

""" -------------------------------------------------------------------------------------------- """



""" --------------------Função que pega o nome do arquivo de entrada------------------------------ """
def getParam():
    return sys.argv[1]

""" -------------------------------------------------------------------------------------------- """



""" ----------------Pega os dados do arquivo e coloca em um vetor-------------------------------- """
def getData(file):
    data = []
    for line in file:
        data.append(line)
    return data

""" -------------------------------------------------------------------------------------------- """



""" -----------------Função que pega os dados necessários para construir/inicializar a tabela----- """
def getInfoInit(data):
    initTable = []

    for line in data:
        if line == '\n':
            break
        else:
            initTable.append(line)
    
    return initTable

""" -------------------------------------------------------------------------------------------- """



""" -------------------Função que pega os dados necessários para efetuar o redo------------------ """
def getRedoInfos(data):
    redoInfos = []
    data.reverse()

    for line in data:
        if line == '\n':
            break
        else:
            redoInfos.append(line)
    
    return redoInfos

""" -------------------------------------------------------------------------------------------- """


""" --------------------------------------Iteração REDO----------------------------------------- """
# NADA PRONTO
""" def parserRedo(redoInfos):
    for line in redoInfos:
        line = line.split(' ')
        id = int(line[0])
        A = int(line[1])
        B = int(line[2])
        insereBanco(id, A, B) """

""" ------------------------------------------------------------------------------------------ """



""" ----------------------Verifica se existe objeto dado ID por parâmetro---------------------- """
def getLinha(id, linhas):
    for linha in linhas:
        if linha.id == id:      
            return linha
    
    return None 

""" ------------------------------------------------------------------------------------------ """


""" --------------Parseamento das informações iniciais para preencher a tabela---------------- """
def parserInfoInit(infoInit):

    linhas = []

    for line in infoInit:
        print(line)
        linha = Linha()

        line1 = line.split(',')

        coluna = line1[0]
        line2 = line1[1].split('=')
        valor = int(line2[1])
        id = int(line2[0])


        linhaTemp = getLinha(id, linhas)

        if linhaTemp == None:


            linha.setId(id)

            if coluna == 'A':
                linha.setColunaA(valor)
            elif coluna == 'B':
                linha.setColunaB(valor)
            
            linhas.append(linha)
        else:
            if coluna == 'A':
                linhaTemp.setColunaA(valor)
            elif coluna == 'B':
                linhaTemp.setColunaB(valor)
    
    return linhas
        
""" ------------------------------------------------------------------------------------------ """           


""" -----------------------------Percorre vetor e insere no banco------------------------------ """
""" def nomedafuncao(linhas):
    for linha in linhas:
        id = linha.id
        A = linha.colunaA
        B = linha.colunaB
        insereBanco(id, A, B)
         """

""" ------------------------------------------------------------------------------------------ """ 


""" ---------------------------------Criar Tabela log------------------------------------------ """
def createTable():
    sql = 'DROP TABLE IF EXISTS log'
    executa_db(sql)
    sql = 'CREATE TABLE log (id INTEGER PRIMARY KEY, colunaA INTEGER, colunaB INTEGER);'
    executa_db(sql)

""" -------------------------------------------------------------------------------------------- """

table = createTable() # Cria a tabela log (id, colunaA, colunaB)
file = openFile(getParam()) # Abrindo arquivo de log
data = getData(file) # Pegando dados do arquivo e colocando em um vetor
initTable = getInfoInit(data) # Pegando os dados para preencher a tabela
redoInfos = getRedoInfos(data) # Pegando os dados para fazer o REDO
tuplas = parserInfoInit(initTable)



print("\nDados totais do arquivo:\n")
printFile(data)
print("\nDados para adicionar na tabela:\n")
printFile(initTable)
print("\nDados para fazer o REDO:\n")
printFile(redoInfos)
print("\nDados parseados\n")


file.close()

