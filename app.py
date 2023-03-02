#   Código Desenvolvido por @Luis Felipe Barbosa
#   1 de Março de 2023
#   Linkedin: https://www.linkedin.com/in/luis-felipe-barbosa-38b994129/
#   GitHub: https://github.com/Dusbeat
#   Vídeo Demonstrativo: https://www.youtube.com/watch?v=Md1Ua2bsfFQ&ab_channel=LuisFelipeBarbosa

from flask import Flask, request, render_template, redirect, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
import psycopg2.extensions
import locale
import os
import re


#   Configurações Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/ifinance'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

#   Configurando POSTGRESQL com PSYCOPG
con = psycopg2.connect (
    host="localhost",
    database="ifinance",
    user="postgres",
    password='admin'
)

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#   Configurando Locale para Moeda Brasileira
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

#   Configurando Session(Cookie)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

cur = con.cursor() # Definindo Cursor SQL

#           Página de Login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"] # Armazenando o valor inserido no campo "Usuario" em uma variável.
        password = request.form["password"] # Armazenando o valor inserido no campo "Senha" em uma variável.

        # Verificando se os campos "Usuario" foram preenchidos.
        if not request.form["email"]:
            return render_template("login.html", msg="Você precisa inserir um Email válido.")
        
        # Verificando se os campos "Senha" foram preenchidos.
        if not request.form["password"]:
            return render_template("login.html", msg="Você precisa inserir a sua senha")
        
        #   Verificando se o Usuário existe no Banco de Dados
        cur.execute("SELECT * FROM usuarios WHERE email = %s", [email])
        row = cur.fetchall()
        if len(row) != 1:
            return render_template("login.html", msg="Não existe uma conta com esse email.")
        
        #   Verificando se a senha coincide com a do Banco de Dados
        cur.execute("SELECT password FROM usuarios WHERE email = %s", [email])
        row = cur.fetchall()
        if password != row[0][0]:
            return render_template("login.html", msg="O Endereço de Email ou Senha não estão corretos.")
        
        #   Se tudo ocorrer bem, o login será feito.
        cur.execute("SELECT id FROM usuarios WHERE email = %s", [email])
        row = cur.fetchall()
        session["user_id"] = row[0][0]
        return redirect('/')

    return render_template("login.html")


#           Página de Registro
@app.route ('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        #   Armazenando valores dos campos em variáveis
        name = request.form["nome"] # Nome
        sobrenome = request.form["sobrenome"] # Sobrenome
        email = request.form["email"] # Email
        email_confirm = request.form["email-confirm"] # Confirmação de Email
        password = request.form["password"] # Senha
        password_confirm = request.form["password-confirm"] # Confirmação de Senha

        #   Verificando Campos Preenchidos

        #   Campo de Nome
        if not request.form["nome"]:
            return render_template("register.html", msg="Você deve informar um Nome")
        
        #   Campo de Sobrenome
        if not request.form["sobrenome"]:
            return render_template("register.html", msg="Você deve informar um Sobrenome")
        
        #   Campo de Email
        if not request.form["email"]:
            return render_template("register.html", msg="Você deve informar um Email para acesso.")
        
        #   Campo de Confirmação de Email
        if not request.form["email-confirm"]:
            return render_template("register.html", msg="Você deve confirmar o seu Endereço de Email.")
        
        #   Campo de Senha
        if not request.form["password"]:
            return render_template("register.html", msg="Você deve informar uma Senha")
        
        #   Campo de Confirmação de Senha
        if not request.form["password-confirm"]:
            return render_template("register.html", msg="Você deve confirmar a sua Senha.")
        

        #   Verificando se as Confirmações Coincidem
        if email != email_confirm:
            return render_template("register.html", msg="Os Endereços de Email não coincidem.")
        
        if password != password_confirm:
            return render_template("register.html", msg="As Senhas não coincidem.")
        

        #   Verificação de Dados Duplicados no Banco de Dados
        cur.execute("SELECT * from usuarios WHERE email = %s", [email])
        row = cur.fetchall()

        if len(row) != 0:
            return render_template("register.html", msg="O Email já se encontra Registrado.")
        
        #   Caso o registro seja feito com sucesso
        cur.execute("INSERT INTO usuarios(nome, sobrenome, email, password, saldo) VALUES (%s, %s, %s, %s, 0)", [name, sobrenome, email, password])
        con.commit()
        return render_template("register.html", msg="Seu registro foi feito com Sucesso! Agora basta iniciar sua sessão em 'Login'")


    return render_template("register.html")


#           Página Inicial
@app.route('/', methods=["GET", "POST"])
def index():
    #Verificando se o Usuário está logado
    if not session.get("user_id"):
        #   Caso não esteja logado, retornar para página de Login
        return redirect('/login')
    
    user_id = session.get("user_id")
    saldo_despesa = 0
    saldo_receita = 0

    # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    cur.execute("SELECT * FROM receitas WHERE id = %s ORDER BY t_number DESC", [user_id])
    row = cur.fetchall()
    receitas = row

    cur.execute("SELECT * FROM despesas WHERE id = %s ORDER BY t_number DESC", [user_id])
    row = cur.fetchall()

    # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    despesas = row     
    
    # Somando Receita Totais
    cur.execute("SELECT * FROM receitas WHERE id = %s", [user_id])
    row = cur.fetchall()
    soma_receita = 0
    for i in row:

        # Transformando STR em INT para fazer os calculos
        n = i[4]
        n = n[3:-3]
        n = int(re.sub(r'[,.]', '', n))
        soma_receita = soma_receita + n
        saldo_receita = soma_receita 

    # Transformando INT em String Monetária
    soma_receita = locale.currency(soma_receita, grouping=True, symbol=None)

        # Somando Despesas Totais
    cur.execute("SELECT * FROM despesas WHERE id = %s", [user_id])
    row = cur.fetchall()
    soma_despesa = 0
    for i in row:

        # Transformando STR em INT para fazer os calculos
        n = i[4]
        n = n[3:-3]
        n = int(re.sub(r'[,.]', '', n))
        soma_despesa = soma_despesa + n    
        saldo_despesa = soma_despesa

    # Transformando INT em String Monetária
    soma_despesa = locale.currency(soma_despesa, grouping=True, symbol=None)

    
    saldo_total = saldo_receita - saldo_despesa  
    saldo = locale.currency(saldo_total, grouping=True, symbol=None)

    if request.method == "POST":

        
        #   Variáveis de Receitas
        descricao_receita = request.form.get("descricao-receita")
        valor_receita = request.form.get("valor-receita")
        data_receita = request.form.get("data-receita")

        #   Variáveis de Despesas
        descricao_despesa = request.form.get("descricao-despesa")
        valor_despesa = request.form.get("valor-despesa")
        data_despesa = request.form.get("data-despesa")

        #   Verificando se a entrada de dados vai ser de Receita ou Despesa
        if not valor_receita:
            btn_receita = False     
        else:
            btn_receita = True

        #   Caso esteja enviando uma Receita
        if btn_receita == True:
            if not valor_receita:
                return render_template("index.html", msg="Você precisa inserir um valor de descricao.", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)
            
            if not descricao_receita:
                return render_template("index.html", msg="Você precisa inserir uma Descrição., receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa")
            
            if not data_receita:
                return render_template("index.html", msg="Você precisa inserir uma Data.", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)
            
            cur.execute("INSERT INTO receitas(id, data, description, valor) VALUES(%s,%s,%s,%s)", [user_id, data_receita, descricao_receita, valor_receita])
            con.commit()

            # Aumentando Saldo do Usuário
            cur.execute("SELECT saldo FROM usuarios WHERE id = %s", [user_id])
            row = cur.fetchall()
            saldo_atual = row[0][0]
            saldo_atualizado = int(saldo_atual) + int(valor_receita)

            # Atualizando valor do Saldo no SQL
            cur.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", [saldo_atualizado, user_id])
            con.commit()
            
           
        
        #   Caso esteja enviando uma Despesa
        else:
            if not valor_despesa:
                return render_template("index.html", msg="Você precisa inserir um valor de despesa.", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)
            
            if not descricao_despesa:
                return render_template("index.html", msg="Você precisa inserir uma Descrição.", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)
            
            if not data_despesa:
                return render_template("index.html", msg="Você precisa inserir uma Data.", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)
            
            # Verificando se existe saldo para despesa
            cur.execute("SELECT saldo FROM usuarios WHERE id = %s", [user_id])
            row = cur.fetchall()
            saldo_atual = row[0][0]

            if int(saldo_atual) < int(valor_despesa):
                return render_template("index.html", msg="O seu saldo é baixo demais para essa Despesa", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)            

            # Diminuindo Saldo do Usuário
            saldo_atualizado = int(saldo_atual) - int(valor_despesa)

            # Atualizando valor do Saldo no SQL
            cur.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", [saldo_atualizado, user_id])
            con.commit()

            # Inserindo Despesa no Banco de DADOS
            cur.execute("INSERT INTO despesas(id, data, description, valor) VALUES(%s,%s,%s,%s)", [user_id, data_despesa, descricao_despesa, valor_despesa])
            con.commit()
            
           

        return redirect("/")
    return render_template("index.html", receitas=receitas, despesas=despesas, saldo=saldo, soma_receita=soma_receita, soma_despesa=soma_despesa)

@app.route('/receitas', methods=["GET", "POST"])
def receitas():

    #Verificando se o Usuário está logado
    if not session.get("user_id"):
        #   Caso não esteja logado, retornar para página de Login
        return redirect('/login')
    
    user_id = session.get("user_id")

     # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    cur.execute("SELECT * FROM receitas WHERE id = %s ORDER BY t_number DESC", [user_id])
    row = cur.fetchall()
    receitas = row

    return render_template("receitas.html", receitas=receitas)

@app.route('/receitas/delete/<int:t_number>', methods=["POST"])
def receitas_Excluir(t_number: int):
    if request.method == "POST":
        cur.execute("DELETE FROM receitas WHERE t_number = %s", [t_number])
        con.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route('/receitas/update/<int:t_number>', methods=["GET", "POST"])
def receitas_Update(t_number: int):
    #Verificando se o Usuário está logado
    if not session.get("user_id"):
        #   Caso não esteja logado, retornar para página de Login
        return redirect('/login')

     # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    cur.execute("SELECT * FROM receitas WHERE t_number = %s", [t_number])
    row = cur.fetchall()
    receitas = row[0]
    valor_receita = receitas[4][2:]
    valor_receita = valor_receita[:-2]
    valor_receita = int(re.sub(r'[,.]', '', valor_receita))

    if request.method == "POST":
        description = request.form["description"]
        valor = request.form["valor"]

        cur.execute("UPDATE receitas SET description=%s, valor=%s WHERE t_number = %s;", [description, valor, t_number])
        con.commit()
        return redirect('/')

    return render_template("editar_receita.html", receitas=receitas, valor_receita=valor_receita)


@app.route('/despesas', methods=["GET", "POST"])
def despesas():

    #Verificando se o Usuário está logado
    if not session.get("user_id"):
        #   Caso não esteja logado, retornar para página de Login
        return redirect('/login')
    
    user_id = session.get("user_id")

     # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    cur.execute("SELECT * FROM despesas WHERE id = %s ORDER BY t_number DESC", [user_id])
    row = cur.fetchall()
    despesas = row

    return render_template("despesas.html", despesas=despesas)

@app.route('/despesas/delete/<int:t_number>', methods=["POST"])
def despesas_Excluir(t_number: int):
    if request.method == "POST":
        cur.execute("DELETE FROM despesas WHERE t_number = %s", [t_number])
        con.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route('/despesas/update/<int:t_number>', methods=["GET", "POST"])
def despesas_Update(t_number: int):
    #Verificando se o Usuário está logado
    if not session.get("user_id"):
        #   Caso não esteja logado, retornar para página de Login
        return redirect('/login')

     # Armazenando Receitas do SQL em Banco de Dados para Aparecer no Front-End
    cur.execute("SELECT * FROM despesas WHERE t_number = %s", [t_number])
    row = cur.fetchall()
    despesas = row[0]
    valor_despesa = despesas[4][2:]
    print(valor_despesa)
    valor_despesa = valor_despesa[:-2]
    print(valor_despesa)
    valor_despesa = int(re.sub(r'[,.]', '', valor_despesa))
    print(valor_despesa)

    if request.method == "POST":
        description = request.form["description"]
        valor = request.form["valor"]

        cur.execute("UPDATE despesas SET description=%s, valor=%s WHERE t_number = %s;", [description, valor, t_number])
        con.commit()
        return redirect('/')

    return render_template("editar_despesas.html", despesas=despesas, valor_despesa=valor_despesa)
