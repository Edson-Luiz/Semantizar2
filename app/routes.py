# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from app import *

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

@app.route('/cadastroLivro', methods=['GET', 'POST'])
def cadastroLivro():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autor = request.form['autor']
            ano = request.form['ano']
            editora = request.form['editora']
            isbn = request.form['isbn']

            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AutorPublicacao=autor,
                AnoPublicacao=ano,
            )
            db.session.add(nova_publicacao)
            db.session.flush()  # Obtem o ID da publicacao

            novo_livro = Livro(
                Editora=editora,
                ISBN=isbn,
                IDPublicacao=nova_publicacao.IDPublicacao
            )
            db.session.add(novo_livro)
            db.session.commit()
            
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('cadastroLivro'))
        except Exception as e:
            return f"Erro ao cadastrar livro: {e}"
    return render_template('cadastroLivro.html')


@app.route('/cadastroArtigo', methods=['GET', 'POST'])
def cadastroArtigo():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autor = request.form['autor']
            ano = int(request.form['ano'])
            revista = request.form['revista']
            volume = int(request.form['volume'])
            numero = int(request.form['numero'])
            paginas = request.form['paginas']
            doi = request.form['doi']

            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AutorPublicacao=autor,
                AnoPublicacao=ano,
            )
            db.session.add(nova_publicacao)
            db.session.flush()  # Obtem o ID da publicacao

            novo_artigo = Artigo(
                Revista=revista,
                Volume=volume,
                Numero=numero,
                Paginas=paginas,
                DOI=doi,
                IDPublicacao=nova_publicacao.IDPublicacao
            )
            db.session.add(novo_artigo)
            db.session.commit()

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('cadastroArtigo'))
        except Exception as e:
            return f"Erro ao cadastrar artigo: {e}"
    return render_template('cadastroArtigo.html')

@app.route('/cadastroDocAcademico', methods=['GET', 'POST'])
def cadastroDocAcademico():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autor = request.form['autor']
            ano = int(request.form['ano'])
            sigla_universidade = request.form['sigla_universidade']
            instituicao = request.form['instituicao']
            tipo_defesa = request.form['tipo_defesa']

            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AutorPublicacao=autor,
                AnoPublicacao=ano,
            )
            db.session.add(nova_publicacao)
            db.session.flush()

            novo_doc = DocAcademico(
                InstituicaoDefesa=instituicao,
                TipoDefesa=tipo_defesa,
                IDPublicacao=nova_publicacao.IDPublicacao
            )
            db.session.add(novo_doc)
            db.session.commit()

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('cadastroDocAcademico'))
        except Exception as e:
            return f"Erro ao cadastrar documento acadêmico: {e}"
    return render_template('cadastroDocAcademico.html')

@app.route('/cadastroRelacao')
def cadastroRelacao():
    return render_template('cadastroRelacao.html')



    

