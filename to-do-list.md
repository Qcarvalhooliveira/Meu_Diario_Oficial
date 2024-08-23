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

(x) Para buscar as informações no diario oficial usaremos python , baixaremos o arquivo para leitura dos dados e na manhã seguinte esse PDF evera ser deletado. (não precisamos deletar porque não estamos baixando estamos lendo online)

(x) Uma logica para buscar similaridades entre o arquivo baixado e os dados do usuario que estarão no banco de dados.

(x) Criar logica de alerta para quando o nome do usuario estiver presente no documento baixado, ele sra notificado por email.

() Criar o email de alerta e atualizar o dashboard. (email criado)

(x) Criar testes unitarios para cada funcionalidade.

(x) Download PDF.(lendo online)

(x) Extração do texto. (leitura sendo feita)

(x) Correspondência de dados. 

(x) Envio de notificação.

() Testes de integração.

() Assegurar que os componentes e as funcionalidades interagam corretamente.

(x) Teste de leitura do diario oficial.

(x) Simular PDF de 500 paginas. (não precisa porque estamos testando com o diario real)

(x) Transformar as letras do user name em minusculas na função task, pois no pdf pode esta escrito de varias formas.

(x) Criar um array de nomes, para que eles sejam verificados no PDF.

(x) Criar uma função para que o PDF não seja lido dia de sabado e domingo.


## importante

sabendo que o email esta sendo enviado fazer:
(x)limpar arquivo init para não enviar mais o email ao ser iniciado. (verificar se esta tudo certo)
(x)verificar o arquivo email
(x)verificar arquivo tasks
(x)fazer o teste funcionar
(x)colocar o horario que o programa vai fazer a leitura do PDF
(x)criar email do aplicativo
(x)modificar o arquivo task para enviar o email para ususarios
(x)criar usuarios com postman
(x)quando a pessoa se inscrever ela deve receber um email confirmando que ele esta inscrito (parabens voce esta inscrito em nossa lista)
(x) verificar se esta lendo e enviando email para TODOS cadastrados
(x) user id tem que ser random string
(x) fazer senha para usuarios e ela tem que ser hashed.
(x) fazer rotas de login - protegida
(x) fazer token de login
(x) bug fix - esta mandando email duas vezes aparentemente resolvido mas precisa ver em outros dias
() modificar temporariamente a rota de get ou o banco de dados para permitir ver a senha armazenada para saber se ela esta mesmo sendo hasheada 
(x) fazer testes do backend
(x) padronizar o email

(x) README falar dos testes
(x) README falar de como os arquivos funcionam para as funções principais. talvez em comentarios nos proprios arquivos. coisa como cada rota funciona, como funciona a leitura do pdf. ver arquivo por arquivo e explicar as principais coisas de cada um deles.
(x) README explicar o fluxo padrão da aplicaçao - cadastro => rodar task => encontrar match => envio de email um outro para não achar match e um outro para se o app não rodar a task
() atualizar o docker (ele roda as migrations?) e explicar como usar o app usando o docker e não com a instalação padrão e rodando o python run.py
(x) README falar as tecnologias usadas nessa aplicação backend (elas estão no topo desse arquivo)
