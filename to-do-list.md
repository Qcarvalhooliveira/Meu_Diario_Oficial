Portfolio Projeto de conclusão de curso

* Nome do Projeto: Meu_Diario_Oficial

* Técnologias à serem utilizadas: 

- Front-end: React TS, HTML, CSS
- Back-end: Python, Flask, Flask-SQLAlchemy, pypdf, requests, pytest, pytest-flask, seleniumls

* Objetivo do Projeto: 

Extrair dados diretamente do Diario Oficial de Salvador e enviar uma notificação via email para os convocados no concurso. Esses usuarios terão que estar cadastrados no nosso banco de dados com nome completo, email, RG e talvez CPF, pois podem haver homonimos.
Se der tempo faremos uma lista de todos os concursos que o usuario foi chamado atraves do google.

* Comportamento do programa:

O programa vai baixar o diario oficial de Salvador todo dia pela manhã à partir de 12:00hs.
Depois que ele baixar o arquivo com sucesso (* Se o programa não conseguir baixar na primeira tentativa, ele vai tentar mais duas vezes a cada 1h e se apos as três tentativas ele não conseguir, o programa enviara um alerta para o usuario, pedindo que a verificação do nome na lista seja feita manualmente) ele vai ler todo o documento, procurando o nome do usuario e CPF (os 5 primeiros digitos).
Se o programa encontrar o nome do usuario, ele vai mandar um alerta em forma de mensagem (email), avisando que o nome foi encontrado na lista e que o usuario deve verificar no diario oficial.
Com a realização de um novo cadastro de usuario, o sistema enviara uma mensagem dizendo que não é possivel realizar o teste no primeiro dia, então o usuario tera que verificar o sistema manualmente no primeiro dia.


* O que iremos precisar para esse aplicativo web?

() Interface para cadastro do usuario e dashboard

() Banco de dados para guardar as informações do usuario como: nome completo, RG, CPF, senha e email.

() Para buscar as informações no diario oficial usaremos python , baixaremos o arquivo para leitura dos dados e na manhã seguinte esse PDF evera ser deletado.

() Uma logica para buscar similaridades entre o arquivo baixado e os dados do usuario que estarão no banco de dados.

() Criar logica de alerta para quando o nome do usuario estiver presente no documento baixado, ele sra notificado por email.

() Criar o email de alerta e atualizar o dashboard.

() Criar testes unitarios para cada funcionalidade.

() Download PDF.

() Extração do texto.

() Correspondência de dados.

() Envio de notificação.

() Testes de integração.

() Assegurar que os componentes e as funcionalidades interagam corretamente.

() Teste de carga.

() Simular PDF de 500 paginas.

() Transformar as letras do user name em minusculas na função task, pois no pdf pode esta escrito de varias formas.

() Criar um array de nomes, para que eles sejam verificados no PDF.

() Criar uma função para que o PDF não seja lido dia de sabado e domingo.


## importante

sabendo que o email esta sendo enviado fazer:
limpar arquivo init para ão enviar mais o email ao ser iniciado. (verificar se esta tudo certo)
verificar o arquivo email
verificar arquivo tasks
fazer o teste funcionar