from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livro_doacao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Enable CORS for all routes
CORS(app)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API de Doação de Livros"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Database Models
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    data_cadastro = db.Column(db.String(10), nullable=False)

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    usuario_doador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario_receptor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    data_doacao = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(20), default='disponivel')  # disponivel ou doado
    data_cadastro = db.Column(db.String(10), nullable=False)

# Helper functions
def formatar_data(data):
    if isinstance(data, str):
        return data
    return data.strftime('%d/%m/%Y')

# Routes
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
    Cadastrar um novo usuário
    """
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data or 'email' not in data:
            return jsonify({
                'erro': 'Campos nome e email são obrigatórios'
            }), 400
        
        nome = data['nome']
        email = data['email']
        
        # Verificar se email já existe
        if Usuario.query.filter_by(email=email).first():
            return jsonify({
                'erro': 'Email já cadastrado'
            }), 400
        
        data_cadastro = formatar_data(datetime.now())
        
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            data_cadastro=data_cadastro
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso',
            'id': novo_usuario.id,
            'nome': nome,
            'email': email,
            'data_cadastro': data_cadastro
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@app.route('/buscar_usuario/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    """
    Buscar usuário por ID
    """
    try:
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_cadastro': usuario.data_cadastro
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    """
    Cadastrar um novo livro para doação
    """
    try:
        data = request.get_json()
        
        if not data or 'titulo' not in data or 'autor' not in data or 'usuario_doador_id' not in data:
            return jsonify({
                'erro': 'Campos titulo, autor e usuario_doador_id são obrigatórios'
            }), 400
        
        titulo = data['titulo']
        autor = data['autor']
        usuario_doador_id = data['usuario_doador_id']
        
        # Verificar se usuário existe
        usuario = Usuario.query.get(usuario_doador_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        data_cadastro = formatar_data(datetime.now())
        
        novo_livro = Livro(
            titulo=titulo,
            autor=autor,
            usuario_doador_id=usuario_doador_id,
            data_cadastro=data_cadastro,
            status='disponivel'
        )
        
        db.session.add(novo_livro)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Livro cadastrado com sucesso',
            'id': novo_livro.id,
            'titulo': titulo,
            'autor': autor,
            'usuario_doador_id': usuario_doador_id,
            'data_cadastro': data_cadastro,
            'status': 'disponivel'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@app.route('/livros_disponiveis', methods=['GET'])
def listar_livros_disponiveis():
    """
    Listar todos os livros disponíveis para doação
    """
    try:
        livros = Livro.query.filter_by(status='disponivel').all()
        
        lista_livros = []
        for livro in livros:
            lista_livros.append({
                'id': livro.id,
                'titulo': livro.titulo,
                'autor': livro.autor,
                'usuario_doador_id': livro.usuario_doador_id,
                'data_cadastro': livro.data_cadastro
            })
        
        return jsonify({
            'total': len(lista_livros),
            'livros': lista_livros
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/doar_livro', methods=['POST'])
def doar_livro():
    """
    Realizar a doação de um livro
    """
    try:
        data = request.get_json()
        
        if not data or 'livro_id' not in data or 'usuario_receptor_id' not in data:
            return jsonify({
                'erro': 'Campos livro_id e usuario_receptor_id são obrigatórios'
            }), 400
        
        livro_id = data['livro_id']
        usuario_receptor_id = data['usuario_receptor_id']
        
        # Verificar se livro existe e está disponível
        livro = Livro.query.get(livro_id)
        if not livro:
            return jsonify({'erro': 'Livro não encontrado'}), 404
        
        if livro.status != 'disponivel':
            return jsonify({'erro': 'Livro não está disponível para doação'}), 400
        
        # Verificar se receptor existe
        usuario_receptor = Usuario.query.get(usuario_receptor_id)
        if not usuario_receptor:
            return jsonify({'erro': 'Usuário receptor não encontrado'}), 404
        
        # Atualizar livro
        livro.usuario_receptor_id = usuario_receptor_id
        livro.data_doacao = formatar_data(datetime.now())
        livro.status = 'doado'
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Doação realizada com sucesso',
            'livro_id': livro.id,
            'titulo': livro.titulo,
            'usuario_doador_id': livro.usuario_doador_id,
            'usuario_receptor_id': livro.usuario_receptor_id,
            'data_doacao': livro.data_doacao
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@app.route('/deletar_livro/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    """
    Deletar um livro (apenas se estiver disponível)
    """
    try:
        livro = Livro.query.get(livro_id)
        
        if not livro:
            return jsonify({'erro': 'Livro não encontrado'}), 404
        
        if livro.status != 'disponivel':
            return jsonify({
                'erro': 'Não é possível deletar livro que já foi doado'
            }), 400
        
        # Deletar livro
        db.session.delete(livro)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Livro deletado com sucesso',
            'id': livro_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """
    Listar todos os usuários cadastrados
    """
    try:
        usuarios = Usuario.query.all()
        
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'data_cadastro': usuario.data_cadastro
            })
        
        return jsonify({
            'total': len(lista_usuarios),
            'usuarios': lista_usuarios
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
