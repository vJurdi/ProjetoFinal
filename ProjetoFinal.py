# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:05:43 2018

@author: Victor Jurdi & Victor Habib

Projeto Final de Design de Software


"""

from flask import Flask, render_template, request
app = Flask(__name__)

itens=[]
logins=[]


from firebase import firebase
firebase = firebase.FirebaseApplication('https://projetofinal-dessoft.firebaseio.com/',None)
if firebase.get('/',None) is None:
    arquivo_firebase = {}
else:
    arquivo_firebase=firebase.get('/',None)

if 'Achados_Perdidos' not in arquivo_firebase:
    arquivo_firebase['Achados_Perdidos']=[]
for e in arquivo_firebase['Achados_Perdidos']:
    itens.append(e)
if 'login' not in arquivo_firebase:
    arquivo_firebase['login']=[]
for o in arquivo_firebase['login']:
    logins.append(o)
    

    
@app.route("/home", methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    




@app.route("/achados_perdidos", methods=['POST', 'GET'])
def Achados_Perdidos():
    mensagem_erro_nome= ''
    mensagem_erro_item = ''
    mensagem_erro_data = ''
    mensagem_erro_lugar = ''
        

    if request.method == 'POST':
        nome = request.form['nome']
        item = request.form['item']
        data = request.form['data']
        lugar = request.form['lugar']
        
        novo_item = {
            'id':len(itens),
            'nome': nome,
            'item': item,
            'data': data,
            'lugar': lugar,
            'encontrado': False,
        }
        tem_erro = False
        if len(nome)==0:
            mensagem_erro_nome= 'Favor insira o nome do proprietário, caso não saiba digite n'
            tem_erro=True
        if len(item)==0:
            mensagem_erro_item='Favor digite qual item foi encontrado'
        if len(data) == 0:
            mensagem_erro_data = 'Favor inserir uma data'
            tem_erro = True
        if len(lugar)==0:
            mensagem_erro_lugar = 'Lugar não pode ser vazio'
            tem_erro = True
        if not tem_erro:
            #idd=len(itens)
            #arquivo_firebase['Achados_perdidos'][idd]=novo_item
            itens.append(novo_item)
            arquivo_firebase['Achados_Perdidos']=itens
            firebase.patch('https://projetofinal-dessoft.firebaseio.com/', arquivo_firebase )

        
    return render_template('achados_perdidos.html', itens=itens,
                           mensagem_erro_nome=mensagem_erro_nome,
                           mensagem_erro_item=mensagem_erro_item,
                           mensagem_erro_data=mensagem_erro_data,
                           mensagem_erro_lugar=mensagem_erro_lugar)
    
@app.route("/salas", methods=['POST', 'GET'])
def Mapa():
    mensagem_erro_sala=''
    planta_sala=''
    
    if request.method == 'POST':
        
        sala = request.form['sala']

        erro=False
        if len(sala)==0:
            mensagem_erro_sala='Escolha uma sala'
            erro=True
        elif sala not in arquivo_firebase['Salas']:
            mensagem_erro_sala='Esta sala não existe'
            erro=True
        for andar in arquivo_firebase['Salas']:
            for salaa in arquivo_firebase['Salas'][andar]:
                for name in arquivo_firebase['Salas'][andar][salaa]:
                    if sala == arquivo_firebase['Salas'][andar][salaa]['nome']:
                        planta_sala=arquivo_firebase['Salas'][andar][salaa]['img']
        
            
    return render_template('Salas.html', itens=itens,mensagem_erro_sala=mensagem_erro_sala,planta_sala=planta_sala)

    
@app.route("/salasft", methods=['POST', 'GET'])
def Mapa1():
    mensagem_erro_sala=''
    planta_sala=''
    
    if request.method == 'POST':
        
        sala = str(request.form['sala'])

        erro=False
        if len(sala)==0:
            mensagem_erro_sala='Escolha uma sala'
            erro=True
        elif sala not in arquivo_firebase['Salas']:
            mensagem_erro_sala='Esta sala não existe'
            erro=True
        for andar in arquivo_firebase['Salas']:
            for salaa in arquivo_firebase['Salas'][andar]:
                for name in arquivo_firebase['Salas'][andar][salaa]:
                    if sala == arquivo_firebase['Salas'][andar][salaa]['nome']:
                        planta_sala=arquivo_firebase['Salas'][andar][salaa]['img']
                        valor_andar = andar
            
    return render_template('Salasft.html', itens=itens,mensagem_erro_sala=mensagem_erro_sala,planta_sala=planta_sala,nome_sala=sala,andar=valor_andar)
        
    
    

    
    

@app.route("/entidade/<id>")
def Entidades(id):
    ent=arquivo_firebase['Entidades']

    return render_template('entidade.html',img=ent[id]['img'],descricao=ent[id]['descriçao'],nome=ent[id]['nome'])


@app.route("/painel", methods=['POST', 'GET'])
def painel():
    return render_template('painel.html')

@app.route("/entidades", methods=['POST', 'GET'])
def entidades():
    return render_template('entidades.html')

@app.route("/contato", methods=['POST', 'GET'])
def contato():
    return render_template('contato.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    home = ''
    if request.method == 'POST':
        for username in arquivo_firebase['login']:
            
            
            if request.form['username']  not in arquivo_firebase['login'].keys() or request.form['password'] != arquivo_firebase['login'][username]['senha']:
                error = 'Login ou senha inválido. Tente novamente.'
            else:
                home='home'
                
    return render_template('login.html', error=error, home=home)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    login = 'cadastro'
    if request.method == 'POST':
        username=request.form['username1']
        senha=request.form['password1']
        
        novo_login = {
            username:{'id':len(logins),
            'senha': senha,
        },
        }
            
        erroo=False   
        if username in arquivo_firebase['login'].keys() :
            error = 'Este nome de usuário já existe.'
            erroo=True
        if len(request.form['senha'])<5:
            error = 'A sua senha deve ter no mínimo 5 caracteres'
            erroo=True
        if not erroo:
            login='mensagem'
            logins.append(novo_login)
            arquivo_firebase['login']=logins
            firebase.patch('https://projetofinal-dessoft.firebaseio.com/', arquivo_firebase )
                
                
    return render_template('cadastro.html', error=error, login=login)

@app.route("/mensagem", methods=['POST', 'GET'])
def mensagem():
    return render_template('mensagem_sucesso.html')


    
app.run('0.0.0.0', 5004, False)





