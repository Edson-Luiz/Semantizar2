# app/routes.py
from flask import render_template
from app import app

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')
def test_db():
    try:
        # Tenta conectar ao banco e listar as tabelas
        result = db.engine.execute("SHOW TABLES;")
        tables = [row[0] for row in result]
        return f"Tabelas no banco de dados: {tables}"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {str(e)}"

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para a página "Contato"
@app.route('/contato')
def contato():
    return render_template('contato.html')

