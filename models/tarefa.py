from app import db
from datetime import datetime, timezone

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
