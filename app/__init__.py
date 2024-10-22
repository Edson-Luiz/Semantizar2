# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa o app Flask
app = Flask(__name__)

# Configurações básicas (adicionar configurações de MySQL mais tarde)
app.config['SECRET_KEY'] = 'chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:senha@localhost/seu_banco_de_dados'

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy(app)

from app import routes  # Importa as rotas

# Iniciar a aplicação
def create_app():
    return app


