# app/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from isbnlib import is_isbn10, is_isbn13, canonical
import requests , PyPDF2, io, itertools
from app import app, jsonify, db, Autor, DocAcademico, Publicacao, Livro, Universidade, Artigo, AutorPublicacao, Relacao, TipoRelacao, PublicacaoRelacao, Substantivo
import os
import uuid
import spacy
import re
import tqdm
import unidecode
from flask_session import Session
from werkzeug.utils import secure_filename
from collections import defaultdict
from itertools import combinations


UPLOAD_FOLDER = 'uploads'  # Pasta para armazenar arquivos enviados
ALLOWED_EXTENSIONS = {'pdf'}

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

nlp = spacy.load("pt_core_news_sm")
nlp.max_length = 5000000 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_last_uploaded_file():
    try:
        # Lista os arquivos na pasta de uploads
        files = os.listdir(UPLOAD_FOLDER)
        
        # Filtra apenas arquivos e ignora diretórios
        files = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        
        if not files:
            return None  # Retorna None se não houver arquivos na pasta
        
        # Ordena os arquivos pela data de modificação (do mais recente para o mais antigo)
        files.sort(key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)), reverse=True)
        
        # Pega o arquivo mais recente
        latest_file = files[0]
        return os.path.join(UPLOAD_FOLDER, latest_file)
    
    except Exception as e:
        print(f"Erro ao tentar pegar o último arquivo: {e}")
        return None

def normalizar_texto(text):
    text = unidecode.unidecode(text)  # Remove acentos
    text = text.lower()  # Tudo em minúsculas
    text = re.sub(r'\s+', ' ', text)  # Substitui múltiplos espaços por um único  
    return text.strip()

# Função para encontrar pares de termos no PDF
def encontrar_pares_termos(pdf_reader, termos):
    pares_encontrados = []
    termo_ocorrencias = defaultdict(list)  # Armazena os índices e frases correspondentes
    frases_total = []  # Lista global para armazenar todas as frases extraídas

    # Extração de texto das páginas do PDF
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            text = normalizar_texto(text)  # Normaliza o texto extraído
            doc = nlp(text)  # Usa o spaCy para segmentar em frases

            # Segmenta corretamente o texto em frases usando o spaCy
            for sent in doc.sents:
                frase = normalizar_texto(sent.text)  # Normaliza cada frase

                frases_total.append(frase)  # Armazena todas as frases

                # Para cada termo, verifica se ele está na frase
                for termo in termos:
                    if normalizar_texto(termo) in frase:  # Verifica se o termo está na frase
                        termo_ocorrencias[termo].append(len(frases_total) - 1)

    # Comparação apenas entre pares de termos
    for termo1, termo2 in itertools.combinations(termos, 2):  # Apenas pares de termos
        frases_comuns = set(termo_ocorrencias[termo1]) & set(termo_ocorrencias[termo2])  # Interseção de frases

        for i in frases_comuns:
            if i < len(frases_total):  # Verifica se o índice é válido
                pares_encontrados.append({
                    "termo1": termo1,
                    "termo2": termo2,
                    "frase": frases_total[i]
                })

    print(f"📌 Total de frases analisadas: {len(frases_total)}")
    print(f"📌 Ocorrências de termos: {dict(termo_ocorrencias)}")
    print(f"✅ Pares encontrados: {pares_encontrados}")

    return pares_encontrados


@app.route("/process_file", methods=["POST"])
def process_file():
    print("Requisição chegou")
    if "file" not in request.files:
        print("Nenhum arquivo chegou")
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]  # Obtém o arquivo enviado
    print(f"Arquivo recebido: {file.filename}")

    if file.filename == "":
        return jsonify({"error": "Nome do arquivo inválido"}), 400

    if file and allowed_file(file.filename):  # Verifica se é um PDF
        # Gera um nome único para o arquivo e salva no servidor
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{filename}")
        file.save(file_path)

        # Retorna o caminho do arquivo para o frontend
        return jsonify({"file_path": file_path}), 200

    return jsonify({"error": "Apenas arquivos PDF são suportados"}), 400


@app.route('/salvar_termos', methods=['POST'])
def salvar_termos():
    termos = []

    # Verifica se um arquivo foi enviado
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo enviado."}), 400
        
        # Verifica se o arquivo é um .txt
        if file and file.filename.endswith('.txt'):
            # Lê os termos do arquivo
            termos = file.read().decode('utf-8').splitlines()
        else:
            return jsonify({"error": "Apenas arquivos .txt são permitidos."}), 400
    else:
        data = request.get_json()
        termos = data.get('termos', [])

    # Verifica se a lista de termos está vazia
    if not termos:
        return jsonify({"error": "Nenhum termo foi enviado."}), 400

    # Verifica se há um arquivo PDF válido salvo
    file_path = get_last_uploaded_file()

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Nenhum arquivo PDF encontrado."}), 400

    print(f"📂 Último arquivo salvo: {file_path}")

    # Abre o arquivo PDF e processa as páginas com tratamento de erro
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        if len(pdf_reader.pages) == 0:
            return jsonify({"error": "O arquivo PDF está vazio."}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao ler o PDF: {str(e)}"}), 400

    # Busca pares de termos no PDF
    pares_encontrados = encontrar_pares_termos(pdf_reader, termos)

    # Salva os resultados na sessão
    session['relacoes_encontradas'] = pares_encontrados
    session['termos'] = termos

    print("Relacoes encontradas:", session.get('relacoes_encontradas'))
    print("Termos:", session.get('termos'))

    # Redireciona para a página de validação
    return redirect(url_for('validacaoRelacao'))



@app.route("/salvar_validacao", methods=["POST"])
def salvar_validacao():
    data = request.get_json()
    termo1 = data.get("termo1")
    termo2 = data.get("termo2")
    is_valid = data.get("isValid")

    # Aqui você pode salvar no banco de dados ou exibir no console
    status = "Aceito" if is_valid else "Rejeitado"
    print(f"🔹 Relação {status}: {termo1} ↔ {termo2}")

    return jsonify({"message": f"Relação {status} com sucesso!"}), 200

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/validacaoRelacao')
def validacaoRelacao():
    # Recupera as relações de termos encontradas da sessão
    relacoes = session.get("relacoes_encontradas", [])

    # Assegura que a chave 'validado' existe em todas as relações
    for relacao in relacoes:
        if 'validado' not in relacao:
            relacao['validado'] = False  # Define 'validado' como False inicialmente

    # Atualiza a sessão
    session['relacoes_encontradas'] = relacoes

    # Filtra as relações não validadas
    relacoes_pendentes = [r for r in relacoes if not r['validado']]

    print(relacoes_pendentes)  # Você pode remover isso após o teste

    return render_template('validacaoRelacao.html', relacoes=relacoes_pendentes)



@app.route('/validarRelacao', methods=['POST'])
def validarRelacao():
    try:
        # Recupera os dados enviados
        dados = request.get_json()
        termo1 = dados['termo1']
        termo2 = dados['termo2']
        frase = dados['frase']

        # Recupera as relações de termos encontradas da sessão
        relacoes = session.get("relacoes_encontradas", [])

        # Atualiza o status de validação da relação
        for relacao in relacoes:
            if relacao['termo1'] == termo1 and relacao['termo2'] == termo2 and relacao['frase'] == frase:
                relacao['validado'] = True

        # Atualiza a sessão
        session['relacoes_encontradas'] = relacoes

        return jsonify({"success": True})

    except Exception as e:
        print(f"Erro ao validar a relação: {str(e)}")
        return jsonify({"success": False, "message": str(e)})


@app.route('/visualizacao')
def visualizacao():
    return render_template('visualizacao.html')

@app.route('/get_relacoes')
def get_relacoes():
    try:
        relacoes = db.session.query(
            Relacao.IDPalavraSujeito,
            Substantivo.NomeSubstantivo.label("termo1"),
            Relacao.Predicado,
            Substantivo.NomeSubstantivo.label("termo2")
        ).join(Substantivo, Relacao.IDPalavraObjeto == Substantivo.IDSubstantivo) \
        .order_by(Relacao.IDRelacao.desc()) \
        .limit(10).all()

        resultado = [{"termo1": r.termo1, "predicado": r.Predicado, "termo2": r.termo2} for r in relacoes]

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

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

@app.route('/salvar_autores', methods=['POST'])
def salvar_autores():
    autores = request.form.getlist('autores[]')
    print(autores)
    session['autores'] = autores  # Armazena os autores na sessão
    return jsonify({"message": "Autores salvos"})

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            # Recebe os dados enviados via JSON

            tipo = request.form['tipo']  # Identifica se é livro, artigo ou doc acadêmico
            titulo = request.form['titulo']
            # Recebe os autores do corpo da requisição JSON
            autores = session.pop('autores', [])
            if not autores:  # Verifica se a lista está vazia
                flash("Erro: A publicação precisa ter pelo menos um autor. (Clique em adicionar pessoas autoras)", "danger")
                return redirect(url_for('cadastro'))
            
            print("Autores recebidos:", autores)
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


@app.route('/cadastroRelacao', methods=['GET', 'POST'])
def cadastroRelacao():
    # Captura os dados passados pela URL
    termo1 = request.args.get('termo1', type=str)
    termo2 = request.args.get('termo2', type=str)
    frase = request.args.get('frase', type=str)

    print(f"URL recebida: {request.url}")
    print(f"Termo1: {repr(termo1)}")
    print(f"Termo2: {repr(termo2)}")
    print(f"Frase: {repr(frase)}")

    if request.method == 'POST':
        try:
            # Garantir que os valores não sejam None, já que podem vir via GET
            termo1 = request.form.get('termo1', termo1)
            termo2 = request.form.get('termo2', termo2)
            frase = request.form.get('frase', frase)

            print(f"Valores recebidos: termo1={termo1}, termo2={termo2}, frase={frase}")

            if not termo1 or not termo2:
                raise ValueError("Os termos não podem ser nulos!")
            
            # Verificar se os termos já existem na tabela Substantivo
            termo1_existente = db.session.query(Substantivo).filter_by(NomeSubstantivo=termo1).first()
            termo2_existente = db.session.query(Substantivo).filter_by(NomeSubstantivo=termo2).first()

            # Se o termo1 não existir, criar novo
            if not termo1_existente:
                termo1_existente = Substantivo(NomeSubstantivo=termo1)
                db.session.add(termo1_existente)

            # Se o termo2 não existir, criar novo
            if not termo2_existente:
                termo2_existente = Substantivo(NomeSubstantivo=termo2)
                db.session.add(termo2_existente)

            # Commit para salvar os termos no banco de dados
            db.session.commit()

            # Captura os dados do formulário
            predicado = request.form.get('relacao')
            tipo_relacao_nome = request.form.get('tiporelacao')
            relacao_inversa = request.form.get('relacao-inversa')
            simetrica = request.form.get('simetrica') == 'sim'
            reflexiva = request.form.get('reflexiva') == 'sim'

            tipo_relacao = TipoRelacao.query.filter_by(NomeTipoRelacao=tipo_relacao_nome).first()
            id_tipo_relacao = tipo_relacao.IDTipoRelacao if tipo_relacao else None

            # Criar a nova relação
            nova_relacao = Relacao(
                IDPalavraSujeito=termo1_existente.IDSubstantivo,
                Predicado=predicado,
                IDPalavraObjeto=termo2_existente.IDSubstantivo,
                IDTipoRelacao=id_tipo_relacao,
                RelacaoInversa=relacao_inversa,
                Simetrica=simetrica,
                Reflexiva=reflexiva,
            )

            db.session.add(nova_relacao)
            db.session.commit()

            flash("Relação cadastrada com sucesso!", "success")
            return redirect(url_for('validacaoRelacao'))

        except Exception as e:
            db.session.rollback()
            print(f"Erro ao cadastrar a relação: {str(e)}")
            flash(f"Erro ao cadastrar a relação: {str(e)}", "danger")
            return redirect(url_for('cadastroRelacao', termo1=termo1, termo2=termo2, frase=frase))

    return render_template('cadastroRelacao.html', termo1=termo1, termo2=termo2, frase=frase)



    



    