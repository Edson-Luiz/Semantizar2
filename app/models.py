from flask_sqlalchemy import SQLAlchemy
from app.__init__ import db
# Definição do modelo Publicacao
class Publicacao(db.Model):
    __tablename__ = 'tbPublicacao'

    IDPublicacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TituloPublicacao = db.Column(db.String(200), nullable=False)
    AutorPublicacao = db.Column(db.String(100), nullable=False)
    OrientadorPublicacao = db.Column(db.String(100))
    CoorientadorPublicacao = db.Column(db.String(100))
    AnoPublicacao = db.Column(db.Integer, nullable=False)
    DiretorioPublicacao = db.Column(db.LargeBinary)
    DiretorioEstruturaPublicacao = db.Column(db.LargeBinary)
    TipoPublicacao = db.Column(db.String(30))
    SiglaUniversidade = db.Column(db.String(30), db.ForeignKey('tbUniversidade.SiglaUniversidade'))

    # Relacionamento com a tabela Universidade
    universidade = db.relationship('Universidade', backref='publicacoes')

# Definição do modelo Universidade
class Universidade(db.Model):
    __tablename__ = 'tbUniversidade'

    SiglaUniversidade = db.Column(db.String(30), primary_key=True)
    NomeUniversidade = db.Column(db.String(100), nullable=False)

# Definição de outros modelos (tbSubstantivo, tbRelacao, etc.) seguem o mesmo padrão.
