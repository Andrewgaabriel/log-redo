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

- *Nome da função + O que ela faz*  
`codigo aqui`

- *Nome da função + O que ela faz*  
`codigo aqui`

- *Nome da função + O que ela faz*  
`codigo aqui`




<div id='como-testar'/>

## **Como testar/executar:**

- *Como executar/descrição de como executar*  
`codigo aqui`




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

