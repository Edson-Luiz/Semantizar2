from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)

# Configurações básicas (adicionar configurações de MySQL mais tarde)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:edsonabc12312@localhost/semantizar2_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy()

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


