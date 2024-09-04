from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone

app = Flask(__name__)

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/teclatdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo para a tabela 'tarefas'
class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    status_conclusao = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    data_status_conclusao = db.Column(db.DateTime, nullable=True)

    def concluir(self):
        self.status_conclusao = True
        self.data_status_conclusao = datetime.now(timezone.utc)

# Rota principal
@app.route('/')
def index():
    tarefas = Tarefa.query.order_by(Tarefa.data_criacao).all()
    return render_template('index.html', tarefas=tarefas, message='')


# Rota API para Criar Tarefa
@app.route('/api/add_task', methods=['POST'])
def add_task_api():
    data = request.json
    task_name = data.get('taskName')
    task_description = data.get('taskDescription')
    
    if task_name and task_description:
        nova_tarefa = Tarefa(titulo=task_name, descricao=task_description)
        db.session.add(nova_tarefa)
        db.session.commit()
        
        response = {
            'id': nova_tarefa.id,
            'titulo': nova_tarefa.titulo,
            'descricao': nova_tarefa.descricao,
            'status_conclusao': nova_tarefa.status_conclusao,
            'data_criacao': nova_tarefa.data_criacao.strftime('%d/%m/%Y %H:%M:%S'),
            'data_status_conclusao': nova_tarefa.data_status_conclusao.strftime('%d/%m/%Y %H:%M:%S') if nova_tarefa.data_status_conclusao else None
        }
        return jsonify(response), 201
    else:
        return jsonify({'error': 'Nome e descrição da tarefa são obrigatórios.'}), 400


# Rota API para Atualizar Tarefa
@app.route('/api/update_task/<int:task_id>', methods=['POST'])
def update_task_api(task_id):
    data = request.json
    task = Tarefa.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404
    
    task.titulo = data.get('taskTitle')
    task.descricao = data.get('taskDescription')
    
    if data.get('taskStatus'):
        task.concluir()
    else:
        task.status_conclusao = False
        task.data_status_conclusao = None
    
    db.session.commit()
    
    response = {
        'id': task.id,
        'titulo': task.titulo,
        'descricao': task.descricao,
        'status_conclusao': task.status_conclusao,
        'data_status_conclusao': task.data_status_conclusao.strftime('%d/%m/%Y %H:%M:%S') if task.data_status_conclusao else None
    }
    return jsonify(response)

# Rota API para Deletar Tarefa
@app.route('/api/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tarefa = Tarefa.query.get(task_id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
        return jsonify({'message': 'Tarefa excluída com sucesso!'}), 200
    return jsonify({'message': 'Tarefa não encontrada!'}), 404


if __name__ == '__main__':
    app.run(debug=True)
