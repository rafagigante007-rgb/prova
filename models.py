# models.py
from flask_sqlalchemy import SQLAlchemy

# 1. Cria a instância do SQLAlchemy para gerenciar a base de dados
db = SQLAlchemy()

# 2. Tabela de Categorias
class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Cria a ligação (1 para N): Uma categoria pode ter vários produtos associados
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

# 3. Tabela de Produtos
class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), default='padrao.png') # Nome da imagem (com imagem padrão se vazia)
    
    # Chave estrangeira: Conecta obrigatoriamente cada produto ao ID de uma Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)