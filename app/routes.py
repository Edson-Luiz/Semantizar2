# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from isbnlib import is_isbn10, is_isbn13, canonical
import requests
from app import app, jsonify, db, Autor, DocAcademico, Publicacao, Livro, Universidade, Artigo
import os
from werkzeug.utils import secure_filename


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Criar o diretório de uploads, se necessário
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file.save(filepath)
            return filepath
        return None
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return None
    

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

@app.route('/cadastroTermos')
def cadastroTermos():
    return render_template('cadastroTermos.html')

@app.route('/processoExtracaoSemantica')
def processoExtracaoSemantica():
    return render_template('processoExtracaoSemantica.html')


@app.route('/salvar_termos', methods=['POST'])
def salvar_termos():
    data = request.get_json()  # Obtém os dados enviados como JSON
    termos = data.get('termos', [])  # Extrai o vetor de termos

    if not termos:
        return jsonify({"error": "Nenhum termo foi enviado."}), 400

    # Aqui você pode processar os termos (ex: salvar no banco de dados)
    print("Termos recebidos:", termos)

    # Retorna uma resposta de sucesso
    return jsonify({"message": "Termos recebidos com sucesso!", "termos": termos}), 200
        
@app.route('/cadastroLivro', methods=['GET', 'POST'])
def cadastroLivro():
    if request.method == 'POST':
        try:
            # Obtendo os dados do formulário
            titulo = request.form['titulo']
            autores = request.form.getlist('autor[]')  # Lista de autores
            ano = request.form['ano']
            editora = request.form['editora']
            isbn = request.form['isbn']

            # Validação do ISBN
            isbn_canonico = canonical(isbn)  # Remove formatações adicionais
            if not (is_isbn10(isbn_canonico) or is_isbn13(isbn_canonico)):
                flash("ISBN inválido! Verifique os dados inseridos.", "error")
                return redirect(url_for('cadastroLivro'))

            # Criando a nova publicação
            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AnoPublicacao=ano,
                AutorPublicacao=", ".join(autores)  # Armazena os autores como string
            )
            db.session.add(nova_publicacao)
            db.session.flush()  # Obtém o ID da publicação

            # Criando e associando os autores ao livro
            for autor in autores:
                # Verifica se o autor já existe, se não, cria um novo autor
                if autor:
                    autor_existente = Autor.query.filter_by(NomeAutor=autor).first()
                    if not autor_existente:
                        novo_autor = Autor(NomeAutor=autor)
                        db.session.add(novo_autor)
                        db.session.flush()  # Obtém o ID do novo autor
                        autor_existente = novo_autor  # Atualiza a variável autor_existente

                    # Associar o autor à publicação
                    nova_publicacao.autores.append(autor_existente)

            db.session.commit()

            novo_livro = Livro(
                Editora=editora,
                ISBN=isbn,
                IDPublicacao=nova_publicacao.IDPublicacao
            )
            db.session.add(novo_livro)
            db.session.commit()

            if 'file' not in request.files:
                flash("Nenhum arquivo enviado", "error")
                return redirect(url_for('cadastroLivro'))
    
            file = request.files['file']
            filepath = save_file(file)
    
            if filepath:
                # Sucesso no cadastro do arquivo
                flash("Cadastro realizado com sucesso!", "success")
                return redirect(url_for('cadastroTermos'))  # Redireciona para a tela de termos
            else:
                flash("Arquivo inválido, envie um PDF", "error")
                return redirect(url_for('cadastroLivro'))  # Retorna para a tela de cadastro com erro

        except Exception as e:
            flash(f"Erro ao cadastrar livro: {str(e)}", "error")
            return redirect(url_for('cadastroLivro'))

    # Renderiza o template de cadastro
    return render_template('cadastroLivro.html')


@app.route('/cadastroArtigo', methods=['GET', 'POST'])
def cadastroArtigo():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autores = request.form.getlist('autor[]')
            ano = int(request.form['ano'])
            revista = request.form['revista']
            volume = int(request.form['volume'])
            numero = int(request.form['numero'])
            doi = request.form['doi']

            # Verificação do DOI
            crossref_url = f"https://api.crossref.org/works/{doi}"
            doi_response = requests.get(crossref_url)
            
            if doi_response.status_code != 200:
                flash("DOI inválido ou não encontrado.", "danger")
                return redirect(url_for('cadastroArtigo'))

            # Criação da publicação
            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AnoPublicacao=ano,
                AutorPublicacao=", ".join(autores)
            )
            db.session.add(nova_publicacao)
            db.session.flush()
            
            # Criando e associando os autores ao artigo
            for autor in autores:
                if autor:
                    autor_existente = Autor.query.filter_by(NomeAutor=autor).first()
                    if not autor_existente:
                        novo_autor = Autor(NomeAutor=autor)
                        db.session.add(novo_autor)
                        db.session.flush()
                        autor_existente = novo_autor

                    nova_publicacao.autores.append(autor_existente)

            db.session.commit()

            # Criação do artigo
            novo_artigo = Artigo(
                Revista=revista,
                Volume=volume,
                Numero=numero,
                DOI=doi,
                IDPublicacao=nova_publicacao.IDPublicacao
            )
            db.session.add(novo_artigo)
            db.session.commit()

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('cadastroTermos'))
        except Exception as e:
            db.session.rollback()
            return f"Erro ao cadastrar artigo: {e}"
    return render_template('cadastroArtigo.html')


@app.route('/cadastroDocAcademico', methods=['GET', 'POST'])
def cadastroDocAcademico():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autores = request.form.getlist('autor[]')
            ano = int(request.form['ano'])
            universidade_data = request.form['universidade']
            tipo_defesa = request.form['tipo_documento']
            orientador = request.form['orientador']
            coorientador = request.form['coorientador']

            sigla, nome_completo = universidade_data.split(',', 1)

            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AnoPublicacao=ano,
                AutorPublicacao=", ".join(autores)
            )
            db.session.add(nova_publicacao)
            db.session.flush()

            for autor in autores:
                # Verifica se o autor já existe, se não, cria um novo autor
                if autor:
                    autor_existente = Autor.query.filter_by(NomeAutor=autor).first()
                    if not autor_existente:
                        novo_autor = Autor(NomeAutor=autor)
                        db.session.add(novo_autor)
                        db.session.flush()  # Obtém o ID do novo autor
                        autor_existente = novo_autor  # Atualiza a variável autor_existente

                    # Associar o autor à publicação
                    nova_publicacao.autores.append(autor_existente)

            db.session.commit()

            novo_doc = DocAcademico(
                TipoDocAcademico=tipo_defesa,
                IDPublicacao=nova_publicacao.IDPublicacao,
                OrientadorDocAcademico=orientador,
                CoorientadorDocAcademico=coorientador,
                SiglaUniversidade=sigla
            )
            db.session.add(novo_doc)
            db.session.commit()


            nova_universidade = Universidade.query.filter_by(SiglaUniversidade=sigla).first()
            if not nova_universidade:
                nova_universidade = Universidade(
                    SiglaUniversidade=sigla,
                    NomeUniversidade=nome_completo
                )
                db.session.add(nova_universidade)
                db.session.commit()

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('cadastroTermos'))
        except Exception as e:
            return f"Erro ao cadastrar documento acadêmico: {e}"
    return render_template('cadastroDocAcademico.html')

@app.route('/cadastroRelacao')
def cadastroRelacao():
    return render_template('cadastroRelacao.html')



    

