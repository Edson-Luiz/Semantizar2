# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from isbnlib import is_isbn10, is_isbn13, canonical
import requests , PyPDF2, io
from app import app, jsonify, db, Autor, DocAcademico, Publicacao, Livro, Universidade, Artigo, AutorPublicacao
import os
from werkzeug.utils import secure_filename


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

@app.route("/process_file", methods=["POST"])
def process_file():
    print("Requisicao chegou")
    if "file" not in request.files:
        print("Nehum arquivo chegou")
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]  # Obtém o arquivo enviado
    print(f"Arquivo recebido: {file.filename}")

    if file.filename == "":
        return jsonify({"error": "Nome do arquivo inválido"}), 400

    if file and file.filename.endswith(".pdf"):  # Verifica se é um PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))  # Lê o PDF da memória
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])  # Extrai texto

        # Aqui você pode rodar seu algoritmo no texto extraído
        resultado = {"texto_extraido": text[:500]}  # Retorna apenas os primeiros 500 caracteres para visualização

        return jsonify(resultado)  # Envia a resposta para o frontend

    return jsonify({"error": "Apenas arquivos PDF são suportados"}), 400
    
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
        
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            tipo = request.form['tipo']  # Identifica se é livro, artigo ou doc acadêmico
            titulo = request.form['titulo']
            # Garantir que apenas autores não vazios sejam inseridos
            autores = [autor.strip() for autor in request.form.getlist('autor[]') if autor.strip()]
            ano = int(request.form['ano'])

            # Criando a publicação
            nova_publicacao = Publicacao(
                TituloPublicacao=titulo,
                AnoPublicacao=ano,
                AutorPublicacao=", ".join(autores)
            )
            db.session.add(nova_publicacao)
            db.session.commit()  # Realiza o commit para garantir o ID da publicação

            # Criando e associando autores
            for autor in autores:
                if autor:
                    autor_existente = Autor.query.filter_by(NomeAutor=autor).first()
                    if not autor_existente:
                        novo_autor = Autor(NomeAutor=autor)
                        db.session.add(novo_autor)
                        db.session.flush()
                        autor_existente = novo_autor

                    # Verifica se a combinação de autor e publicação já existe
                    autor_publicacao_existente = db.session.query(AutorPublicacao).filter_by(IDAutor=autor_existente.IDAutor, IDPublicacao=nova_publicacao.IDPublicacao).first()

                    if not autor_publicacao_existente:
                        nova_publicacao.autores.append(autor_existente)


            # Tratamento específico por tipo
            if tipo == 'livro':
                editora = request.form['editora']
                isbn = request.form['isbn']

                # Validação do ISBN
                isbn_canonico = canonical(isbn)
                if not (is_isbn10(isbn_canonico) or is_isbn13(isbn_canonico)):
                    flash("ISBN inválido!", "error")
                    return redirect(url_for('cadastro'))

                novo_livro = Livro(
                    Editora=editora,
                    ISBN=isbn,
                    IDPublicacao=nova_publicacao.IDPublicacao
                )
                db.session.add(novo_livro)

            elif tipo == 'artigo':
                revista = request.form['revista']
                volume = int(request.form['volume'])
                numero = int(request.form['numero'])
                doi = request.form['doi']

                # Verificação do DOI
                crossref_url = f"https://api.crossref.org/works/{doi}"
                doi_response = requests.get(crossref_url)

                if doi_response.status_code != 200 or not doi_response.json().get('message', {}).get('DOI'):
                    flash("DOI inválido ou não encontrado.", "danger")
                    return redirect(url_for('cadastro'))

                novo_artigo = Artigo(
                    Revista=revista,
                    Volume=volume,
                    Numero=numero,
                    DOI=doi,
                    IDPublicacao=nova_publicacao.IDPublicacao
                )
                db.session.add(novo_artigo)

            elif tipo == 'doc_academico':
                universidade_data = request.form['universidade']
                tipo_defesa = request.form['tipo_documento']
                orientador = request.form['orientador']
                coorientador = request.form['coorientador']

                try:
                    sigla, nome_completo = universidade_data.split(',', 1)
                except ValueError:
                    flash("Formato inválido para universidade", "error")
                    return redirect(url_for('cadastro'))

                novo_doc = DocAcademico(
                    TipoDocAcademico=tipo_defesa,
                    IDPublicacao=nova_publicacao.IDPublicacao,
                    OrientadorDocAcademico=orientador,
                    CoorientadorDocAcademico=coorientador,
                    SiglaUniversidade=sigla
                )
                db.session.add(novo_doc)

                # Verifica se a universidade já existe
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
            db.session.rollback()
            flash(f"Erro ao cadastrar: {e}", "error")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')


@app.route('/cadastroRelacao')
def cadastroRelacao():
    return render_template('cadastroRelacao.html')



    

