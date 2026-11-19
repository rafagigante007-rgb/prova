# app.py
from flask import Flask
from models import db, Categoria
from routes import init_routes

# 1. Inicializa a aplicação Flask
app = Flask(__name__)

# 2. Configura a conexão com o banco de dados SQLite (database.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Liga o banco de dados e as rotas à aplicação
db.init_app(app)
init_routes(app)

# 4. Cria as tabelas e popula as categorias padrão na primeira execução
with app.app_context():
    db.create_all() # Cria as tabelas do SQLite baseadas nos models
    if Categoria.query.count() == 0:
        c1 = Categoria(nome='Eletrônicos')
        c2 = Categoria(nome='Roupas')
        c3 = Categoria(nome='Alimentos')
        db.session.add_all([c1, c2, c3])
        db.session.commit() # Salva as categorias no banco

# 5. Inicia o servidor local de desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)