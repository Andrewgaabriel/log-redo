from cmath import log
import psycopg2
import sys



""" --------------------Estrutura de dados para armazenar as informações do cabeçalho------------ """
class Linha:

    def init(self):
        self.id = 0
        self.columnA = ''
        self.columnB = ''

    def setId(self, id):
        self.id = id

    def setColumnA(self, columnA):
        self.columnA = columnA

    def setColumnB(self, columnB):
        self.columnB = columnB
""" -------------------------------------------------------------------------------------------- """


""" -------------------------------------- GENERAL FUNCTIONS ----------------------------------------- """


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



""" -----------------------Função para imprimir conteúdo de um vetor/lista/arquivo--------------- """
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
    

    redoInfosCleaned = cleanRedoInfos(redoInfos) # faz a limpeza dos dados antes de retornar
    return redoInfosCleaned
""" -------------------------------------------------------------------------------------------- """



""" --------------------------------------Limpa o vetor para manusear---------------------------- """
def cleanRedoInfos(file):
    data = []
    for line in file:
        data.append(line.replace(">", "").replace("<", "").replace("(", " ").replace(")", " ").upper())
    return data
""" -------------------------------------------------------------------------------------------- """



""" ----------------------Verifica se existe objeto dado ID por parâmetro---------------------- """
def getLinhaIndex(id, linhas):

    for linha in linhas:
        if linha.id == id:      
            return linha
    
    return None 
""" ------------------------------------------------------------------------------------------ """



""" --------------Parseamento das informações iniciais para preencher a tabela---------------- """
def parserInfoInit(infoInit):

    vLinhas = []

    for line in infoInit:

        linha = Linha()

        dirtyLine = line.split(',')

        column = dirtyLine[0]
        dirtyLine2 = dirtyLine[1].split('=')
        value = int(dirtyLine2[1])
        id = int(dirtyLine2[0])


        founded = getLinhaIndex(id, vLinhas)

        if founded == None:

            linha.setId(id)

            if column == 'A':
                linha.setColumnA(value)

            elif column == 'B':
                linha.setColumnB(value)
            
            vLinhas.append(linha)

        else:
            if column == 'A':
                founded.setColumnA(value)

            elif column == 'B':
                founded.setColumnB(value)
    
    return vLinhas
        
""" ------------------------------------------------------------------------------------------ """           



""" ----------------------- Inserindo tupla no banco de dados ------------------------------------- """
def insertInDatabase( id, A, B):
    sql = """ INSERT INTO log (id, a, b) VALUES ('%d','%d','%d'); """ % (id, A, B)
    executa_db(sql)
""" -------------------------------------------------------------------------------------------- """



""" -----------------------------Percorre vetor e insere no banco------------------------------ """
def initTable(vLinhas):
    for linha in vLinhas:
        id = linha.id
        A = linha.columnA
        B = linha.columnB
        insertInDatabase(id, A, B)
""" ------------------------------------------------------------------------------------------ """ 



""" ---------------------------------Criar Tabela log------------------------------------------ """
def createTable():
    sql = 'DROP TABLE IF EXISTS log'
    executa_db(sql)
    sql = 'CREATE TABLE log (id INTEGER PRIMARY KEY, a INTEGER, b INTEGER);'
    executa_db(sql)
""" -------------------------------------------------------------------------------------------- """



""" -------------------------------------- REDO FUNCTIONS ----------------------------------------- """



""" ------------------------------------ encontrou um 'START CKPT' --------------------------------- """
def startCheckpointFounded(dirtyLine):

    line = dirtyLine.split(' ')
    cleanLine = line[2].split(',')
    return cleanLine
""" ------------------------------------------------------------------------------------------------ """



""" ------------------------------------ encontrou uma transação ----------------------------------- """
def transactionRedoFounded(dirtyLine):

    line = dirtyLine.replace('\n', '')
    cleanLine = line.split(',')
    return cleanLine
""" ------------------------------------------------------------------------------------------------ """



""" ------------------------------------ encontrou um 'COMMIT' ------------------------------------- """
def commitRedoFounded(dirtyLine):
    
    cleanedLine = dirtyLine.split(' ')
    transaction = cleanedLine[1]
    return transaction
""" ------------------------------------------------------------------------------------------------ """



""" ----------------------------- faz a iteração do mecanismo REDO ---------------------------------- """
def redoIteration(redoInfos):

    #flags and vectors
    toRedo = [] #vetor de transações para fzr o REDO
    transactions = [] #vetor de transações
    startedTransactions = [] 
    openedCkptTransactions = []
    ckptEndFounded = False

    for line in redoInfos:

        if line.startswith('END CKPT'):
            ckptEndFounded = True
            
        if line.startswith('START T'):
            startedTransactions.append(line.replace('START ', '').replace('\n', ''))

        if line.startswith('START CKPT') and ckptEndFounded == True:
            openedCkptTransactions = startCheckpointFounded(line)
            break # para não percorrer o resto do arquivo

        if line.startswith('T'): #guarda as transações encontradas
            transaction = transactionRedoFounded(line)
            transactions.append(transaction)

        if line.startswith('COMMIT'):
            commit = commitRedoFounded(line)
            toRedo.append(commit.replace('\n', '')) # Adiciona a transação ao vetor de transações a serem refeitas

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



""" ----------------------------- faz a impressão da tabela ---------------------------------- """
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
""" -------------------------------------------------------------------------------------------- """



""" --------------- faz a busca das transações que precisam ser refeitas através do vetor toRedo--------------- """
def redoExecution(toRedo,redoInfos):

    toRedoExecution = []
    for redo in toRedo:
        for line in redoInfos:
            if line.startswith(redo):
                transaction = transactionRedoFounded(line)
                toRedoExecution.append(transaction)
    redoTransaction(toRedoExecution)
""" ----------------------------------------------------------------------------------------------------------- """



""" --------------- faz a iteração para verificar se as transações já estão no banco --------------------------- """
def redoTransaction(toRedoExecution):
    toRedoExecution.reverse() # verificar se a versão correta do dado é a do último commit
    for transaction in toRedoExecution:

        if verifyInDatabase(transaction) == True:
            continue
            #print('\n -> Transação já existe no banco de dados')
            
        else:
            #print('\nTransação não existe no banco de dados')
            redoTransactionExecution(transaction) 
""" ----------------------------------------------------------------------------------------------------------- """



""" ------------------------------------------- faz a verificação no banco de dados --------------------------- """
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
""" ---------------------------------------------------------------------------------------------------------- """



""" ------------------------------------------- executa a transação que precisa fazer o REDO ----------------- """
def redoTransactionExecution(transaction):
    #print('... Executando transação: ', transaction)

    if transaction[2] == 'A':
        sql = """ UPDATE log SET A = '%d' WHERE id = '%d'; """ % (int(transaction[3]), int(transaction[1]))
        executa_db(sql)
    elif transaction[2] == 'B':
        sql = """ UPDATE log SET B = '%d' WHERE id = '%d'; """ % (int(transaction[3]), int(transaction[1]))
        executa_db(sql)
    else:
        print('\n !!! Erro ao executar transação - COLUNA INEXISTENTE \n')
""" ---------------------------------------------------------------------------------------------------------- """


""" --------------------------------------- EXECUÇÃO PRINCIPAL --------------------------------------------------- """


createTable()                                   # Cria a tabela log (id, columnA, columnB)
file = openFile(getParam(1))                    # Abre o arquivo de entrada
allData = getData(file)                         # Pega os dados do arquivo e coloca em um vetor
header = getInfoInit(allData)                   # Pega os dados do vetor para preencher a tabela
redoInfos = getRedoInfos(allData)               # Pega os dados do vetor para fazer o REDO
tuplas = parserInfoInit(header)                 # Pega os valores a serem inseridos no banco
initTable(tuplas)                               # Insere valores no Banco


""" print("\nDados totais do arquivo:\n")
printFile(data)
print("\nDados para adicionar na tabela:\n")
printFile(header)
print("\nDados para fazer o REDO:\n")
printFile(redoInfos)
print("\nDados LIMPOS para redo:\n")
printFile(redoInfosCleaned) """

""" print("\nDados da tabela antes do REDO:\n")
printTable(1) # Imprime a tabela log  """


redoIteration(redoInfos) #Executa o REDO
print("\nDados da tabela depois do REDO:\n")
printTable(1)

file.close()

