# Semantizar 2

Semantizar 2 é uma aplicação desenvolvida para facilitar a extração e análise de relações semânticas em documentos acadêmicos. A versão atual está sendo implementada usando o framework **Flask**, com **MySQL** como banco de dados e a biblioteca **spaCy** para processamento de linguagem natural.

## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
semantizar2/
├── app/
│   ├── __init__.py           # Inicialização da aplicação Flask
│   ├── routes.py             # Rotas do Flask
│   ├── templates/            # Arquivos HTML
│   ├── static/               # Arquivos estáticos (CSS, JS)
│   └── models.py             # Definição de modelos (caso necessário)
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

## Dependências

As principais dependências do projeto incluem:

- **Flask**: Framework web para Python.
- **spaCy**: Biblioteca para processamento de linguagem natural.
- **MySQL**: Banco de dados relacional.
- **SQLAlchemy**: ORM para interagir com o MySQL.

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Edson-Luiz/Semantizar2.git
   cd Semantizar2
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados no MySQL e conecte-o no arquivo de configuração do Flask.

5. Execute o servidor:

   ```bash
   flask run
   ```

## Estrutura de Código

### **app/__init__.py**

Este arquivo contém a inicialização do Flask e a configuração de outras dependências do projeto, como o banco de dados e a integração com o spaCy.

```python
from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)


# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/semantizar2_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '###'
relacoes_temporarias = []

# Inicializa o banco de dados (SQLAlchemy)
db = SQLAlchemy()

def create_app():
    from app import routes
    db.init_app(app)
    return app

```

### **app/routes.py**

As rotas responsáveis por processar as requisições do usuário. Aqui você implementa os endpoints para interagir com o sistema.

```python
from flask import render_template, request, redirect, url_for, flash, session
from isbnlib import is_isbn10, is_isbn13, canonical
import requests , PyPDF2, io, itertools
from app import app, jsonify, db, Autor, DocAcademico, Publicacao, Livro, Universidade, Artigo, AutorPublicacao, Relacao, TipoRelacao, PublicacaoRelacao, Substantivo, relacoes_temporarias
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

@app.route('/')
def home():
    return render_template('index.html')

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
```

### **app/templates/index.html**

O arquivo HTML onde o usuário pode interagir com a aplicação.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Semantizar 2</title>
</head>
<body>
    <h1>Semantizar 2</h1>
    <form action="/processar" method="post">
        <textarea name="texto" rows="10" cols="30"></textarea><br>
        <button type="submit">Processar</button>
    </form>
</body>
</html>
```

## Algoritmo de Processamento

O algoritmo que está sendo desenvolvido para o **Semantizar 2** irá processar um arquivo PDF e uma lista de termos em um vetor. Ele irá formar pares de termos (primeiro com o segundo, e assim por diante) e verificará se ambos os termos aparecem na mesma frase do PDF.

1. Carregar o PDF e o vetor de termos.
2. Dividir o PDF em frases.
3. Para cada par de termos:
   - Verificar se ambos os termos estão presentes na mesma frase.
4. Retornar a confirmação com base na análise.

### Exemplo de código para processamento

```python
def processar_termos(pdf_texto, termos):
    # Supondo que 'pdf_texto' seja o texto extraído do PDF
    frases = pdf_texto.split('.')
    
    for i in range(len(termos)):
        for j in range(i+1, len(termos)):
            termo1 = termos[i]
            termo2 = termos[j]
            for frase in frases:
                if termo1 in frase and termo2 in frase:
                    return f"Termos '{termo1}' e '{termo2}' encontrados na mesma frase."
    return "Nenhum par de termos encontrado na mesma frase."
```

## Funcionalidades Futuras

- **Interface de Validação**: O sistema permitirá que o usuário valide os pares de termos encontrados.
- **Mapas Conceituais**: A ideia é criar mapas conceituais para ilustrar as relações semânticas entre os termos.
- **Gráficos de Frequência de Termos**: Será possível visualizar quais termos aparecem com mais frequência no texto.
```
