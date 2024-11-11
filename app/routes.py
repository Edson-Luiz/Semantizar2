# app/routes.py
from flask import render_template, request, redirect, url_for
from app import app
from app.models import db, Publicacao  

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

@app.route('/processar_cadastro', methods=['GET', 'POST'])
def processar_cadastro():
    if request.method == 'POST':
        # Pegando os dados do formulário
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        orientador = request.form.get('orientador')
        ano = request.form.get('ano')
        tipo = request.form.get('tipo')
        sigla_universidade = request.form.get('sigla_universidade')

        # Criando uma nova instância de Publicacao
        nova_publicacao = Publicacao(
            TituloPublicacao=titulo,
            AutorPublicacao=autor,
            OrientadorPublicacao=orientador,
            AnoPublicacao=ano,
            TipoPublicacao=tipo,
            SiglaUniversidade=sigla_universidade
        )
        
        # Salvando no banco de dados
        db.session.add(nova_publicacao)
        db.session.commit()

    return "Publicação cadastrada com sucesso!"

