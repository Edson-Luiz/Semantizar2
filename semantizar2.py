from app import create_app

# Cria a instância da aplicação Flask
app = create_app()

# Executa o servidor se o script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)  # Modo de depuração ativado

