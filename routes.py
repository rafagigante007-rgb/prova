
import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, Produto, Categoria

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}

def permitido_arquivo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def init_routes(app):
    
    @app.route('/')
    def index():
        busca = request.args.get('busca', '')
        if busca:
            # Filtra pelo nome e ordena em ordem alfabética
            produtos = Produto.query.filter(Produto.nome.ilike(f'%{busca}%')).order_by(Produto.nome.asc()).all()
        else:
            produtos = Produto.query.order_by(Produto.nome.asc()).all()
            
        return render_template('index.html', produtos=produtos, busca=busca)

    @app.route('/cadastrar', methods=['GET', 'POST'])
    def cadastrar():
        categorias = Categoria.query.all()
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            preco_str = request.form.get('preco', '')
            categoria_id = request.form.get('categoria_id')
            
            # Trava de segurança: Validação do nome
            if len(nome) < 3:
                flash('O nome do produto deve ter pelo menos 3 caracteres.', 'danger')
                return redirect(url_for('cadastrar'))
            
            # Trava de segurança: Conversão segura do preço
            try:
                preco = float(preco_str)
                if preco <= 0:
                    raise ValueError()
            except ValueError:
                flash('Preço inválido ou menor/igual a zero.', 'danger')
                return redirect(url_for('cadastrar'))
            
            # Tratamento da imagem
            file = request.files.get('imagem')
            nome_arquivo = 'padrao.png'
            
            if file and file.filename != '':
                if permitido_arquivo(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/uploads', filename))
                    nome_arquivo = filename
                else:
                    flash('Extensão de imagem não permitida!', 'danger')
                    return redirect(url_for('cadastrar'))

            novo_produto = Produto(
                nome=nome,
                preco=preco,
                categoria_id=int(categoria_id),
                imagem=nome_arquivo
            )
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
            
        return render_template('form.html', categorias=categorias, produto=None)

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        produto = Produto.query.get_or_404(id)
        categorias = Categoria.query.all()
        
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            preco_str = request.form.get('preco', '')
            categoria_id = request.form.get('categoria_id')
            
            if len(nome) < 3:
                flash('O nome deve ter pelo menos 3 caracteres.', 'danger')
                return redirect(url_for('editar', id=id))
                
            try:
                preco = float(preco_str)
                if preco <= 0:
                    raise ValueError()
            except ValueError:
                flash('Preço inválido.', 'danger')
                return redirect(url_for('editar', id=id))
            
            file = request.files.get('imagem')
            if file and file.filename != '':
                if permitido_arquivo(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/uploads', filename))
                    
                    # Remove a foto antiga do disco se não for a padrão
                    if produto.imagem != 'padrao.png':
                        caminho_antigo = os.path.join('static/uploads', produto.imagem)
                        if os.path.exists(caminho_antigo):
                            os.remove(caminho_antigo)
                            
                    produto.imagem = filename
                else:
                    flash('Extensão de arquivo inválida!', 'danger')
                    return redirect(url_for('editar', id=id))
            
            produto.nome = nome
            produto.preco = preco
            produto.categoria_id = int(categoria_id)
            
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
            
        return render_template('form.html', categorias=categorias, produto=produto)

    @app.route('/excluir/<int:id>')
    def excluir(id):
        produto = Produto.query.get_or_404(id)
        
        # Remove a imagem do disco se não for a padrão
        if produto.imagem != 'padrao.png':
            caminho_imagem = os.path.join('static/uploads', produto.imagem)
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído com sucesso!', 'success')
        return redirect(url_for('index'))