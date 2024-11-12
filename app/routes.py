# app/routes.py
from flask import render_template, request, redirect, url_for
from app import app
 

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para a página "Contato"
@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


    

