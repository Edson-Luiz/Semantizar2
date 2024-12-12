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

@app.route('/validacao')
def validacao():
    return render_template('validacao.html')

@app.route('/visualizacao')
def visualizacao():
    return render_template('visualizacao.html')

# Rota para a página "Contato"
@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastroLivro')
def cadastroLivro():
    return render_template('cadastroLivro.html')

@app.route('/cadastroArtigo')
def cadastroArtigo():
    return render_template('cadastroArtigo.html')

@app.route('/cadastroDocAcademico')
def cadastroDocAcademico():
    return render_template('cadastroDocAcademico.html')

@app.route('/cadastroRelacao')
def cadastroRelacao():
    return render_template('cadastroRelacao.html')



    

