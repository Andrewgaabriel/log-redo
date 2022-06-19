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
                            password='1234')
    return con
""" -------------------------------------------------------------------------------------------- """




""" -------------------Executa algum comando SQL no banco de dados-------------------------------- """
def executa_db(sql):
    con = conectandoBanco()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        con.rollback()
        con.close()
        return 1
    cur.close()

""" -------------------------------------------------------------------------------------------- """


""" -----------------Abrindo arquivo de log------------------------------------------------------- """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        #print('... arquivo aberto com sucesso')
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
def getParam(arg):
    return sys.argv[arg]

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


""" --------------------------------------Limpa entrada----------------------------------------- """
def cleanRedoInfos(file):
    data = []
    for line in file:
        data.append(line.replace(">", "").replace("<", "").replace("(", " ").replace(")", " ").upper())
    return data

""" -------------------------------------------------------------------------------------------- """


""" --------------------------------------Identifica REDO----------------------------------------- """
# Encontrou start
def startCheckpointFounded(dirtyLine):

    line = dirtyLine.split(' ')
    transactions = line[2].split(',')
    return transactions


# Encontrou transação
def transactionRedoFounded(dirtyLine):

    #remove \n
    line = dirtyLine.replace('\n', '')
    transactions = line.split(',')
    return transactions

# Encontrou commit
def commitRedo(dirtyLine):
    
    cleanedLine = dirtyLine.split(' ')
    transaction = cleanedLine[1]
    return transaction

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


""" --------------Inserindo Registro------------------------------------------------------------- """

def insereBanco( id, A, B):
    sql = """ INSERT INTO log (id, a, b) VALUES ('%d','%d','%d'); """ % (id, A, B)
    executa_db(sql)
""" -------------------------------------------------------------------------------------------- """



""" -----------------------------Percorre vetor e insere no banco------------------------------ """
def initTable(linhas):
    for linha in linhas:
        id = linha.id
        A = linha.colunaA
        B = linha.colunaB
        insereBanco(id, A, B)
""" ------------------------------------------------------------------------------------------ """ 



""" ---------------------------------Criar Tabela log------------------------------------------ """
def createTable():
    sql = 'DROP TABLE IF EXISTS log'
    executa_db(sql)
    sql = 'CREATE TABLE log (id INTEGER PRIMARY KEY, a INTEGER, b INTEGER);'
    executa_db(sql)
""" -------------------------------------------------------------------------------------------- """


""" ---------------------------------........------------------------------------------ """

def redoIteration(redoInfos):

    #flags and vectors
    toRedo = [] #vetor de transações para fzr o REDO
    transactions = [] #vetor de transações
    startedTransactions = [] 
    openedCkptTransactions = []
    ckptEndFounded = False
    ckptStartFounded = False

    for line in redoInfos:

        if line.startswith('END CKPT'):
            ckptEndFounded = True
            #print('Encontrou um END CKPT', line)

        if line.startswith('START T'):
            startedTransactions.append(line.replace('START ', '').replace('\n', ''))
            #print('Encontrou um START T', line)    

        if line.startswith('START CKPT') and ckptEndFounded == True: #
            openedCkptTransactions = startCheckpointFounded(line)
            ckptStartFounded = True
            #print('Encontrou um START CKPT', start)

            break # para não percorrer o resto do arquivo

        elif line.startswith('START CKPT') and ckptEndFounded == False:
            #ignora o ckpt
            start = startCheckpointFounded(line)
            ckptStartFounded = False
            #print('Encontrou um START CKPT mas ele não tem fechamento', start)

        if line.startswith('T'): #guarda as transações encontradas
            transaction = transactionRedoFounded(line)
            transactions.append(transaction)
            #print('Encontrou uma transação', transaction)

        if line.startswith('COMMIT'):
            commit = commitRedo(line)
            toRedo.append(commit.replace('\n', '')) # Adiciona a transação ao vetor de transações a serem refeitas
            #print('Encontrou um COMMIT', commit)
    

    """ print('\nAlterações encontradas:', transactions)
    print('Transações abertas no checkpoint:', openedCkptTransactions)
    print('Transações a serem refeitas com o REDO:', toRedo, "\n") """

    
    for i in openedCkptTransactions:
        if i not in toRedo:
            print('Transação', i, 'não realizou o REDO')
    for i in toRedo:
        print('Transação', i, 'realizou o REDO')
    
    redoExecution(toRedo,redoInfos)

""" -------------------------------------------------------------------------------------------- """


def printTable(op):
    sql = 'SELECT * FROM log'
    result = executa_db(sql)
    result.reverse()
    if op == 1:
        for linha in result:
            print('\t',linha[0],',A =',linha[1],'\n','\t',linha[0],',B =',linha[2])
    elif op == 2:
        print('\t----------------------')
        print('\t| ID: \t| A:\t| B: |')
        print('\t----------------------')
        for linha in result:
            print('\t|', linha[0],'\t|', linha[1],'\t|', linha[2],'|')
        print('\t----------------------')


def redoExecution(toRedo,redoInfos):
    toRedoExecution = []
    for redo in toRedo:
        for line in redoInfos:
            if line.startswith(redo):
                #print('linha da transação: ', line.replace('\n', ''))
                transaction = transactionRedoFounded(line)
                #print('Transação a ser refeita:', transaction, '\n\n')
                toRedoExecution.append(transaction)
                #redoTransaction(transaction)
                #break nao da p usar break pq pode ter mais de uma transação a ser refeita
    redoTransaction(toRedoExecution)



def redoTransaction(toRedoExecution):
    toRedoExecution.reverse() # verificar se a versão correta do dado é a do último commit
    for transaction in toRedoExecution:

        if verifyInDatabase(transaction) == True:
            print('\n -> Transação já existe no banco de dados')
            
        else:
            print('\nTransação não existe no banco de dados')
            redoTransactionExecution(transaction) 
        

def verifyInDatabase(transaction):
    if transaction[2] == 'A':
        sql = """ SELECT A FROM log WHERE id = '%d'""" % (int(transaction[1]))
    elif transaction[2] == 'B':
        sql = """ SELECT B FROM log WHERE id = '%d'""" % (int(transaction[1]))

    result = executa_db(sql)

    if result[0][0] == int(transaction[3]):
        return True #não precisa fazer update
    else:
        return False #precisa fazer update

""" -------------------------------------------------------------------------------------------- """


def redoTransactionExecution(transaction):
    print('... Executando transação: ', transaction)

    if transaction[2] == 'A':
        sql = """ UPDATE log SET A = '%d' WHERE id = '%d'; """ % (int(transaction[3]), int(transaction[1]))
        executa_db(sql)
    elif transaction[2] == 'B':
        sql = """ UPDATE log SET B = '%d' WHERE id = '%d'; """ % (int(transaction[3]), int(transaction[1]))
        executa_db(sql)
    else:
        print('\n !!! Erro ao executar transação - COLUNA INEXISTENTE \n')

    







createTable() # Cria a tabela log (id, colunaA, colunaB)
file = openFile(getParam(1)) # Abrindo arquivo de log
data = getData(file) # Pegando dados do arquivo e colocando em um vetor
header = getInfoInit(data) # Pegando os dados para preencher a tabela
redoInfos = getRedoInfos(data) # Pegando os dados para fazer o REDO
tuplas = parserInfoInit(header) #Pega os valores a serem inseridos no banco
initTable(tuplas) #Insere valores no Banco
redoInfosCleaned = cleanRedoInfos(redoInfos) #Limpa o vetor de dados






""" print("\nDados totais do arquivo:\n")
printFile(data)
print("\nDados para adicionar na tabela:\n")
printFile(header)
print("\nDados para fazer o REDO:\n")
printFile(redoInfos)
print("\nDados LIMPOS para redo:\n")
printFile(redoInfosCleaned) """

print("\nDados da tabela antes do REDO:\n")
#printTable(2) # Imprime a tabela log 
redoIteration(redoInfosCleaned) #Executa o REDO
print("\nDados da tabela depois do REDO:\n")
#printTable(2)

file.close()

