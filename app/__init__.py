from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)

# Configurações básicas (adicionar configurações de MySQL mais tarde)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:#@localhost/semantizar2_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy()

class Publicacao(db.Model):
    __tablename__ = 'tbPublicacao'

    IDPublicacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TituloPublicacao = db.Column(db.String(200), nullable=False)
    AutorPublicacao = db.Column(db.String(100), nullable=False)
    OrientadorPublicacao = db.Column(db.String(100))
    CoorientadorPublicacao = db.Column(db.String(100))
    AnoPublicacao = db.Column(db.Integer, nullable=False)
    TipoPublicacao = db.Column(db.String(30))
    SiglaUniversidade = db.Column(db.String(30), db.ForeignKey('tbUniversidade.SiglaUniversidade'))

    # Relacionamento com a tabela Universidade
    universidade = db.relationship('Universidade', backref='publicacoes')

class Universidade(db.Model):
    __tablename__ = 'tbUniversidade'

    SiglaUniversidade = db.Column(db.String(30), primary_key=True)
    NomeUniversidade = db.Column(db.String(100), nullable=False)

@app.route('/cadastrar_publicacao', methods=['GET', 'POST'])
def cadastrar_publicacao():
    if request.method == 'POST':
        # Captura os dados do formulário
        titulo = request.form['titulo']
        autor = request.form['autor']
        orientador = request.form['orientador']
        coorientador = request.form.get('coorientador')
        ano = request.form['ano']
        tipo_publicacao = request.form['tipo_publicacao']
        sigla_universidade = request.form['sigla_universidade']

        # Cria o objeto Publicacao
        nova_publicacao = Publicacao(
            TituloPublicacao=titulo,
            AutorPublicacao=autor,
            OrientadorPublicacao=orientador,
            CoorientadorPublicacao=coorientador,
            AnoPublicacao=ano,
            TipoPublicacao=tipo_publicacao,
            SiglaUniversidade=sigla_universidade
        )

        # Adiciona a nova publicação e comita no banco de dados
        db.session.add(nova_publicacao)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('index')



@app.route("/teste")
def test_db():
    try:
        # Criando uma conexão manual
        with db.engine.connect() as connection:
            result = connection.execute(text('SHOW TABLES;'))
            tables = result.fetchall()
            return f"Tabelas no banco de dados: {tables}"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"

from app import routes  # Importa as rotas

# Iniciar a aplicação
def create_app():
    db.init_app(app)
    return app
