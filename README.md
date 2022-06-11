# **Implementação do mecanismo de Log REDO com checkpoint usando PostgreSQL em Python**

*Implementado por: [Andrew Gabriel](https://github.com/Andrewgaabriel) e [Igor Radkte](https://github.com/IgorRadtke)*

*******


## **Conteúdo:**
1. *[Funções Implementadas](#funções)*
2. *[Como testar/executar ?](#como-testar)*
3. *[Como funciona o mecanismo de Log REDO ?](#mecanismo-de-log-redo)*
4. *[Requisitos](#requisitos)*


*******





<div id='funções'/>  

## **Funções Implementadas:**

   
`conectandoBanco()`: : =  *Faz a conexão entre a aplicação e o banco de dados.*

`executa_db()`: : =  *Efetua um comando SQL com tratamento de erro.*

`insereBanco()`: : =  *Insere o valor passado pelos parâmetros no banco de dados*

`openFile()`: : =  *Abre o arquivo que foi passado por parâmetro*

`printFile()`: : =  *Faz a impressão linha a linha de um vetor/file/lista*

`getParam()`: : =  *Retorna o parâmetro que foi passado na execução da aplicação no terminal*

`getData()`: : =  *Pega os dados presentes no arquivo de entrada e o passa para um vetor de dados*

`getInitTable()`: : =  *Separa do vetor de dados as informações que serão utilizadas na hora de inicializar a tabela*

`getRedoinfos()`: : =  *Separa do vetor de dados as informações que serão utilizadas na hora de executar o REDO*

<!-- `nomedafunção()`: : =  *descrição da função* -->


<div id='como-testar'/>

## **Como testar/executar:**

- **Requisitos:**
    - *Python 3.7*
    - *PostgreSQL*

- **Como executar:**
    - Você deve ter em um diretório o arquivo da aplicação e o arquivo de entrada.
    - Execute o arquivo da aplicação no terminal da seguinte maneira:
        ```
        python3 log-redo.py <arquivo_de_entrada.txt>
        ``` 


<div id='mecanismo-de-log-redo'/>

## **Funcionamento:**

- *Descrição do mecanismo de Log REDO*

<div id='requisitos'/>

## **Requisitos do trabalho acadêmico:**

- **Funções a serem implementadas:**    

    1. Carregar o banco de dados com a tabela antes de executar o código do log (para zerar as configurações e dados parciais);  

    2. Carregar o arquivo de log;

    3. Verifique quais transações devem realizar REDO. Imprimir o nome das transações que irão sofrer Redo. Observem a questão do checkpoint;

    4. Checar quais valores estão salvos nas tabelas (com o select) e atualizar valores inconsistentes (update);

    5. Reportar quais dados foram atualizados;

    6. Seguir o fluxo de execução conforme o método de REDO, conforme visto em aula;

- **Execução:**
    1. Pode ser implementado em duplas;

    2. A nota será individual;

    3. Deve ser enviado o repositório no GIT (será avaliado a participação dos membros através dos commits). Um único commit com o código pronto será entendido como uma cópia e receberá nota zero.  Os commits irão interferir na nota final dos membros da dupla;

    4. Será testado com outro arquivo de log a execução do programa;

