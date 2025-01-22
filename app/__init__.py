from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)
app.secret_key = '9xCq0VHwlW16Pv7CIXWX'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:semant1401@localhost/semantizar2_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy()

# MODELOS DO BANCO DE DADOS
class Universidade(db.Model):
    __tablename__ = 'tbUniversidade'

    SiglaUniversidade = db.Column(db.String(50), primary_key=True)
    NomeUniversidade = db.Column(db.String(255), nullable=False)

    def __init__(self, SiglaUniversidade, NomeUniversidade):
        self.SiglaUniversidade = SiglaUniversidade
        self.NomeUniversidade = NomeUniversidade


class Publicacao(db.Model):
    __tablename__ = 'tbPublicacao'

    IDPublicacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TituloPublicacao = db.Column(db.String(255), nullable=False)
    AutorPublicacao = db.Column(db.String(100), nullable=False)
    AnoPublicacao = db.Column(db.Integer, nullable=False)

    autores = db.relationship('Autor',
                              secondary='tbAutorPublicacao',
                              back_populates='publicacoes')

    def __init__(self, TituloPublicacao, AutorPublicacao, AnoPublicacao):
        self.TituloPublicacao = TituloPublicacao
        self.AutorPublicacao = AutorPublicacao
        self.AnoPublicacao = AnoPublicacao


class Livro(db.Model):
    __tablename__ = 'tbLivro'

    IDLivro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Editora = db.Column(db.String(255), nullable=False)
    ISBN = db.Column(db.String(50), nullable=False)
    IDPublicacao = db.Column(db.Integer,
                             db.ForeignKey('tbPublicacao.IDPublicacao'))

    def __init__(self, Editora, ISBN, IDPublicacao):
        self.Editora = Editora
        self.ISBN = ISBN
        self.IDPublicacao = IDPublicacao


class Artigo(db.Model):
    __tablename__ = 'tbArtigo'

    IDArtigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Revista = db.Column(db.String(255), nullable=False)
    Volume = db.Column(db.Integer)
    Numero = db.Column(db.Integer)
    Paginas = db.Column(db.String(50))
    DOI = db.Column(db.String(255))
    IDPublicacao = db.Column(db.Integer,
                             db.ForeignKey('tbPublicacao.IDPublicacao'))

    def __init__(self, Revista, Volume, Numero, Paginas, DOI, IDPublicacao):
        self.Revista = Revista
        self.Volume = Volume
        self.Numero = Numero
        self.Paginas = Paginas
        self.DOI = DOI
        self.IDPublicacao = IDPublicacao


class DocAcademico(db.Model):
    __tablename__ = 'tbDocAcademico'

    IDDocAcademico = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    TipoDocAcademico = db.Column(db.String(50), nullable=False)
    IDPublicacao = db.Column(db.Integer,
                             db.ForeignKey('tbPublicacao.IDPublicacao'))
    SiglaUniversidade = db.Column(
        db.String(50), db.ForeignKey('tbUniversidade.SiglaUniversidade'))

    OrientadorDocAcademico = db.Column(db.String(255),
                                       nullable=False)  # Obrigatório
    CoorientadorDocAcademico = db.Column(db.String(255),
                                         nullable=True)  # Pode ser nulo

    universidade = db.relationship('Universidade', backref='publicacoes')

    # Relacionamento com a tabela de Publicações
    publicacao = db.relationship('Publicacao',
                                 backref='documentos',
                                 uselist=False)

    def __init__(self, TipoDocAcademico, IDPublicacao, SiglaUniversidade, OrientadorDocAcademico, CoorientadorDocAcademico):
        self.TipoDocAcademico = TipoDocAcademico
        self.IDPublicacao = IDPublicacao
        self.SiglaUniversidade = SiglaUniversidade
        self.OrientadorDocAcademico = OrientadorDocAcademico
        self.CoorientadorDocAcademico = CoorientadorDocAcademico


class AutorPublicacao(db.Model):
    __tablename__ = 'tbAutorPublicacao'

    IDAutor = db.Column(db.Integer,
                        db.ForeignKey('tbAutor.IDAutor'),
                        primary_key=True)
    IDPublicacao = db.Column(db.Integer,
                             db.ForeignKey('tbPublicacao.IDPublicacao'),
                             primary_key=True)

    def __init__(self, IDAutor, IDPublicacao):
        self.IDAutor = IDAutor
        self.IDPublicacao = IDPublicacao


class Autor(db.Model):
    __tablename__ = 'tbAutor'

    IDAutor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NomeAutor = db.Column(db.String(100), nullable=False)

    # Relacionamento muitos para muitos com Publicacao
    publicacoes = db.relationship('Publicacao',
                                  secondary='tbAutorPublicacao',
                                  back_populates='autores')

    def __init__(self, NomeAutor):
        self.NomeAutor = NomeAutor


# Modelo para a tabela tbSubstantivo
class Substantivo(db.Model):
    __tablename__ = 'tbSubstantivo'

    IDSubstantivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NomeSubstantivo = db.Column(db.String(255), nullable=False, unique=True)

    # Relacionamento com tbRelacao
    relacoes_sujeito = db.relationship('Relacao',
                                       backref='substantivo_sujeito',
                                       foreign_keys='Relacao.IDPalavraSujeito',
                                       lazy=True)
    relacoes_objeto = db.relationship('Relacao',
                                      backref='substantivo_objeto',
                                      foreign_keys='Relacao.IDPalavraObjeto',
                                      lazy=True)

    def __repr__(self):
        return f"<Substantivo(ID={self.IDSubstantivo}, Nome='{self.NomeSubstantivo}')>"

    def __init__(self, NomeSubstantivo):
        self.NomeSubstantivo = NomeSubstantivo


# Modelo para a tabela tbRelacao
class Relacao(db.Model):
    __tablename__ = 'tbRelacao'

    IDRelacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDPalavraSujeito = db.Column(db.Integer,
                                 db.ForeignKey('tbSubstantivo.IDSubstantivo'),
                                 nullable=False)
    Predicado = db.Column(db.String(255), nullable=False)
    IDPalavraObjeto = db.Column(db.Integer,
                                db.ForeignKey('tbSubstantivo.IDSubstantivo'),
                                nullable=False)
    IDTipoRelacao = db.Column(db.Integer,
                              db.ForeignKey('tbTipoRelacao.IDTipoRelacao'),
                              nullable=True)
    RelacaoInversa = db.Column(db.String(255), nullable=True)
    Simetrica = db.Column(db.Boolean, nullable=True, default=False)
    Reflexiva = db.Column(db.Boolean, nullable=True, default=False)

    # Relacionamento com tbTipoRelacao (opcional)
    tipo_relacao = db.relationship('TipoRelacao',
                                   backref='relacoes',
                                   lazy=True)

    # Relacionamento com tbPublicacaoRelacao
    publicacao_relacoes = db.relationship('PublicacaoRelacao',
                                          backref='relacao',
                                          lazy=True)

    def __repr__(self):
        return f"<Relacao(ID={self.IDRelacao}, Sujeito={self.IDPalavraSujeito}, Predicado='{self.Predicado}', Objeto={self.IDPalavraObjeto})>"

    def __init__(self, IDPalavraSujeito, Predicado, IDPalavraObjeto, IDTipoRelacao, RelacaoInversa, Simetrica, Reflexiva):
        self.IDPalavraSujeito = IDPalavraSujeito
        self.Predicado = Predicado
        self.IDPalavraObjeto = IDPalavraObjeto
        self.IDTipoRelacao = IDTipoRelacao
        self.RelacaoInversa = RelacaoInversa
        self.Simetrica = Simetrica
        self.Reflexiva = Reflexiva


# Modelo para a tabela tbTipoRelacao
class TipoRelacao(db.Model):
    __tablename__ = 'tbTipoRelacao'

    IDTipoRelacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NomeTipoRelacao = db.Column(db.String(255), nullable=False)
    subTipoRelacaoDe = db.Column(db.Integer,
                                 db.ForeignKey('tbTipoRelacao.IDTipoRelacao'),
                                 nullable=True)

    def __repr__(self):
        return f"<TipoRelacao(ID={self.IDTipoRelacao}, Nome='{self.NomeTipoRelacao}')>"

    def __init__(self, NomeTipoRelacao, subTipoRelacaoDe=None):
        self.NomeTipoRelacao = NomeTipoRelacao
        self.subTipoRelacaoDe = subTipoRelacaoDe


# Modelo para a tabela tbPublicacaoRelacao
class PublicacaoRelacao(db.Model):
    __tablename__ = 'tbPublicacaoRelacao'

    IDRelacao = db.Column(db.Integer,
                          db.ForeignKey('tbRelacao.IDRelacao'),
                          primary_key=True)
    IDPublicacao = db.Column(db.Integer,
                             db.ForeignKey('tbPublicacao.IDPublicacao'),
                             primary_key=True)

    # Relacionamento com tbPublicacao
    publicacao = db.relationship('Publicacao',
                                 backref='publicacao_relacoes',
                                 lazy=True)

    def __repr__(self):
        return f"<PublicacaoRelacao(IDRelacao={self.IDRelacao}, IDPublicacao={self.IDPublicacao})>"


# Inicializa o banco e roda o app
def create_app():
    from app import routes
    db.init_app(app)
    return app
