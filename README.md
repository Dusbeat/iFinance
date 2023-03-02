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

### Propósito do Projeto:
Projeto desenvolvido como etapa final do curso "CS50 - Introduction to Science Computer" de Harvard.
Consiste em uma Aplicação WEB de Gerenciamento Financeiro no qual o usuário final pode:
  - Adicionar, Editar e Excluir Receitas Monetárias
  - Adicionar, Editar e Excluir Despesas
  - Ter um Resumo do seu saldo baseado em suas Receitas + Despesas
  
### Resumo do Projeto:
#### SQL:
Foi criado 3 tabelas no Banco de Dados para armazenar todas as informações.

- Usuarios:
ID Primary Key, Nome, Sobrenome, Email e Senha.

- Receitas:
T_number: Primary Key, ID, Data, Descrição, Valor.

- Despesas:
- T_number, ID, Data, Descrição e Valor.

Importante ressaltar que o "t_number" é um "ID de Transação" único para cada transação adicionado ao Database, dessa forma sempre que for feito uma alteração ou exclusão de dados por parte do Usuário, a aplicação usa o "t_number" como referência da transação alvo de alteração, dessa forma evita que afete outros dados cadastrados.
  
## Dificuldades no Projeto:

### Conversão Monetária:
  Como o Valor das Receitas e Despesas do usuário eram armazenadas no Banco de Dados já formatado como moeda, para fazer a soma de todas as despesas e todas as receitas
  eu iria precisar converter o valor de Monetário para Número Inteiro removendo tanto "R$" quanto as outras acentuações para fazer a soma e depois retornar esse valor em
  formato Monetário novamente na tela do usuário.
  Para chegar a esse Resultado

#### Editar, Excluir Receitas e Despesas:
  Quando adicionei a função de mostrar todas 
