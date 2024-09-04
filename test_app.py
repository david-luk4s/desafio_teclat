import unittest
from app import app, db, Tarefa
from flask import json

class TaskApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/teclatdb_test'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with cls.app.app_context():
            db.create_all()
            cls.task = Tarefa(titulo="Test Task", descricao="Test Description")
            db.session.add(cls.task)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def test_delete_task(self):
        # Verifica se a tarefa foi criada
        response = self.client.get('/api/tarefas')
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertGreater(len(tasks), 0)

        # Deleta a tarefa
        response = self.client.delete(f'/api/delete_task/{self.task.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tarefa excluída com sucesso!', response.data)

        # Verifica se a tarefa foi deletada
        response = self.client.get(f'/api/tarefas/{self.task.id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
