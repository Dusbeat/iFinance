# iFinance
## By. Luis Felipe Barbosa

### Vídeo Demonstrativo: 
https://www.youtube.com/watch?v=Md1Ua2bsfFQ&ab_channel=LuisFelipeBarbosa

### Linguagens / Tecnologias Utilizadas:
#### Front-End:
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

#### Back-End:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

#### Recursos Adicionais Utilizados no Projeto:
  - Psycopg2 : Para fazer a conexão do Banco de Dados entre o Código e o PostgreSQL
  - Locale: Para converter os valores INTEIROS para Formatação de Moeda BRL

## Resumo do Projeto:
Projeto desenvolvido como etapa final do curso "CS50 - Introduction to Science Computer" de Harvard.
Consiste em uma Aplicação WEB de Gerenciamento Financeiro no qual o usuário final pode:
  - Adicionar, Editar e Excluir Receitas Monetárias
  - Adicionar, Editar e Excluir Despesas
  - Ter um Resumo do seu saldo baseado em suas Receitas + Despesas
  
## SQL:
Foi criado 3 tabelas no Banco de Dados para armazenar todas as informações.

- Usuarios:
ID Primary Key, Nome, Sobrenome, Email e Senha.

- Receitas:
T_number: Primary Key, ID, Data, Descrição, Valor.

- Despesas:
 T_number, ID, Data, Descrição e Valor.

Importante ressaltar que o "t_number" é um "ID de Transação" único para cada transação adicionado ao Database, dessa forma sempre que for feito uma alteração ou exclusão de dados por parte do Usuário, a aplicação usa o "t_number" como referência da transação alvo de alteração, dessa forma evita que afete outros dados cadastrados.

## Páginas:

### /login :
 #### "GET":
  Apenas imprime a página "login.html" na tela do usuário.
  
#### "POST":
  Recebe os valores de "Email" e "Senha" efetuando uma pesquisa no Banco de Dados para verificar se o Usuário Existe ou se as informações estão corretas.
  Caso ao contrário retorna um pop-up de alerta com a mensagem do erro.
  
### /register :
 #### "GET":
  Apenas imprime a página "register.html" na tela do usuário.
  
 #### "POST" :
  Recebe os valores inseridos em todos os campos de entrada de dados e armazena em variáveis, iniciando uma verificação de campos para se certificar que todos 
  os campos foram preenchidos e faz uma pesquisa no banco de dados para verificar se o usuário já está registrado.
  Caso passe em todas as verificações, é criado um novo registro para o usuário no banco de dados anexando um ID único ao mesmo.

### / :
 #### "GET":
  Faz uma busca completa no banco de dados para descobrir todas as Receitas, Despesas e Saldo do Usuário para retornar o valor como texto para o Front-End.
 #### "POST":  
  Endpoint para quando o usuário criar uma Nova Receita ou uma Nova Despesa clicando no botão da página. Recebe como a entrada do usuário o Valor, Data e Descrição    da transação logo após insere os novos dados no banco de dados.

### /receitas :
 #### "GET":
  Executa uma busca no banco de dados de todas as transações no formado de Receitas ligadas ao ID do Usuário e imprime da tela do usuário, possibilitando Editar e Excluir qualquer transação.
  
### /despesas :
 #### "GET":
  Executa uma busca no banco de dados de todas as transações no formado de Despesas ligadas ao ID do Usuário e imprime da tela do usuário, possibilitando Editar e Excluir qualquer transação.
  
### /receitas/delete/t_number :
 #### "POST":
  Endpoint definido onde "t_number" é o ID de Transação para cada receita ou despesa. Após ser requisitado esse endpoint no metódo POST, o aplicativo entende que é pra deletar a transação com o "t_number" retornado na URL.
 
### /receitas/update/t_number :
 #### "POST":
  Endpoint definido onde "t_number" é o ID de Transação para cada receita ou despesa. Após ser requisitado esse endpoint no metódo POST, o aplicativo entende que é pra editar a transação com o "t_number" retornado na URL.

### /despesas/delete/t_number :
 #### "POST":
  Endpoint definido onde "t_number" é o ID de Transação para cada receita ou despesa. Após ser requisitado esse endpoint no metódo POST, o aplicativo entende que é pra deletar a transação com o "t_number" retornado na URL.

### /receitas/update/t_number :
 #### "POST":
  Endpoint definido onde "t_number" é o ID de Transação para cada receita ou despesa. Após ser requisitado esse endpoint no metódo POST, o aplicativo entende que é pra editar a transação com o "t_number" retornado na URL.
  
  
## Dificuldades no Projeto:

### Conversão Monetária:
  Como o Valor das Receitas e Despesas do usuário eram armazenadas no Banco de Dados já formatado como moeda, para fazer a soma de todas as despesas e todas as receitas
  eu iria precisar converter o valor de Monetário para Número Inteiro removendo tanto "R$" quanto as outras acentuações para fazer a soma e depois retornar esse valor em
  formato Monetário novamente na tela do usuário.
  Para chegar a esse Resultado utilizei da seguinte lógica:
  #
  ![image](https://user-images.githubusercontent.com/91026386/222460083-4a56abb2-b2e4-42c7-a683-a45a40ae83f2.png)
  #
  
  Utilizei um laço de repetição para descobrir quantas receitas foram geradas no banco de dados no registro daquele usuário, como o valor é retornado em lista utilizei
  o "n = i[4]" para selecionar somente o campo "Valor" da resposta do query, utilizei o "n = n[3:-3]" para remover o "R$" e utilizei o "n = int(re.sub(r'[,.]', '', n))" para remover os caracteres especiais da variável, e logo após transformar em um número inteiro para que eu pudesse fazer a soma e armazenar em "soma_despesa".
  No final utilizo o Locale para transformar o número inteiro em uma String como Valor Monetário formatado em BRL para exibir na tela do usuário.

