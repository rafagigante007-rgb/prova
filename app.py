
from flask import Flask
from models import db, Categoria
from routes import init_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_routes(app)

with app.app_context():
    db.create_all()
    # Garante pelo menos 3 categorias cadastradas se a tabela estiver vazia
    if Categoria.query.count() == 0:
        c1 = Categoria(nome='Eletrônicos')
        c2 = Categoria(nome='Roupas')
        c3 = Categoria(nome='Alimentos')
        db.session.add_all([c1, c2, c3])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)