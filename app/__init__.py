from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)
app.secret_key = '#'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:#@localhost/semantizar2_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy()

# MODELOS DO BANCO DE DADOS
class Universidade(db.Model):
    __tablename__ = 'tbUniversidade'

    SiglaUniversidade = db.Column(db.String(50), primary_key=True)
    NomeUniversidade = db.Column(db.String(255), nullable=False)

class Publicacao(db.Model):
    __tablename__ = 'tbPublicacao'

    IDPublicacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TituloPublicacao = db.Column(db.String(255), nullable=False)
    AutorPublicacao = db.Column(db.String(100), nullable=False)
    AnoPublicacao = db.Column(db.Integer, nullable=False)
   

class Livro(db.Model):
    __tablename__ = 'tbLivro'

    IDLivro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Editora = db.Column(db.String(255), nullable=False)
    ISBN = db.Column(db.String(50), nullable=False)
    IDPublicacao = db.Column(db.Integer, db.ForeignKey('tbPublicacao.IDPublicacao'))

class Artigo(db.Model):
    __tablename__ = 'tbArtigo'

    IDArtigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Revista = db.Column(db.String(255), nullable=False)
    Volume = db.Column(db.Integer)
    Numero = db.Column(db.Integer)
    Paginas = db.Column(db.String(50))
    DOI = db.Column(db.String(255))
    IDPublicacao = db.Column(db.Integer, db.ForeignKey('tbPublicacao.IDPublicacao'))

class DocAcademico(db.Model):
    __tablename__ = 'tbDocAcademico'

    IDDocAcademico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    InstituicaoDefesa = db.Column(db.String(255), nullable=False)
    TipoDefesa = db.Column(db.String(50), nullable=False)
    IDPublicacao = db.Column(db.Integer, db.ForeignKey('tbPublicacao.IDPublicacao'))
    SiglaUniversidade = db.Column(
        db.String(50), db.ForeignKey('tbUniversidade.SiglaUniversidade')
    )
    universidade = db.relationship('Universidade', backref='publicacoes')

from app import routes
# Inicializa o banco e roda o app
def create_app():
    db.init_app(app)
    return app
