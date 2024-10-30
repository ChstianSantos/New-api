import unittest
from app import app, db
from models.aluno import adicionar_aluno, listar_alunos, aluno_por_id, atualizar_aluno, excluir_aluno, Aluno
from models.professor import adicionar_professor, listar_professores, professor_por_id, atualizar_professor, excluir_professor, Professor
from models.turma import adicionar_turma, listar_turmas, turma_por_id, atualizar_turma, excluir_turma, Turma

class TesteProjeto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.client = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.client = app.test_client()
        db.session.query(Aluno).delete()  
        db.session.query(Turma).delete()  
        db.session.query(Professor).delete()  
        db.session.commit()
        self.criar_professor_padrao()
        self.criar_turma_padrao()

    def criar_professor_padrao(self):
        novo_professor = {
            'nome': 'Professor Padrão',
            'idade': 40,
            'materia': 'Matemática',
            'observacoes': 'Teste de professor'
        }
        adicionar_professor(novo_professor)

    def criar_turma_padrao(self):
        professor = listar_professores()[0]
        nova_turma = {
            'descricao': 'Turma Padrão',
            'ativo': True,
            'professor_id': professor['id']
        }
        adicionar_turma(nova_turma)

    def test_adicionar_aluno(self):
        turma = listar_turmas()[0]
        novo_aluno = {
            'nome': 'Teste Aluno',
            'idade': 20,
            'data_nascimento': '2004-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': turma['id']
        }
        adicionar_aluno(novo_aluno)
        alunos = listar_alunos()
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0]['nome'], 'Teste Aluno')

    def test_atualizar_aluno(self):
        turma = listar_turmas()[0]
        novo_aluno = {
            'nome': 'Teste Aluno',
            'idade': 20,
            'data_nascimento': '2004-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': turma['id']
        }
        adicionar_aluno(novo_aluno)
        aluno = listar_alunos()[0]
        atualizar_aluno(aluno['id'], {
            'nome': 'Aluno Atualizado',
            'idade': 21,
            'data_nascimento': '2004-01-01',
            'nota_primeiro_semestre': 9.0,
            'nota_segundo_semestre': 8.5,
            'turma_id': turma['id']
        })
        aluno_atualizado = aluno_por_id(aluno['id'])
        self.assertEqual(aluno_atualizado['nome'], 'Aluno Atualizado')

    def test_excluir_aluno(self):
        turma = listar_turmas()[0]
        novo_aluno = {
            'nome': 'Teste Aluno',
            'idade': 20,
            'data_nascimento': '2004-01-01',
            'nota_primeiro_semestre': 8.0,
            'nota_segundo_semestre': 7.5,
            'turma_id': turma['id']
        }
        adicionar_aluno(novo_aluno)
        aluno = listar_alunos()[0]
        excluir_aluno(aluno['id'])
        alunos = listar_alunos()
        self.assertEqual(len(alunos), 0)

    # Testes para Professor
    def test_atualizar_professor(self):
        professor = listar_professores()[0]
        atualizar_professor(professor['id'], {
            'nome': 'Professor Atualizado',
            'idade': 45,
            'materia': 'Física',
            'observacoes': 'Atualizado'
        })
        professor_atualizado = professor_por_id(professor['id'])
        self.assertEqual(professor_atualizado['nome'], 'Professor Atualizado')

    def test_excluir_professor(self):
        professor = listar_professores()[0]
        excluir_professor(professor['id'])
        professores = listar_professores()
        self.assertEqual(len(professores), 0)

    # Testes para Turma
    def test_adicionar_turma(self):
        professor = listar_professores()[0]
        nova_turma = {
            'descricao': 'Nova Turma',
            'ativo': True,
            'professor_id': professor['id']
        }
        adicionar_turma(nova_turma)
        turmas = listar_turmas()
        self.assertEqual(len(turmas), 2)  
        self.assertEqual(turmas[1]['descricao'], 'Nova Turma')

    def test_atualizar_turma(self):
        turma = listar_turmas()[0]
        professor = listar_professores()[0]
        atualizar_turma(turma['id'], {
            'descricao': 'Turma Atualizada',
            'ativo': False,
            'professor_id': professor['id']
        })
        turma_atualizada = turma_por_id(turma['id'])
        self.assertEqual(turma_atualizada.descricao, 'Turma Atualizada')

    def test_excluir_turma(self):
        turma = listar_turmas()[0]
        excluir_turma(turma['id'])
        turmas = listar_turmas()
        self.assertEqual(len(turmas), 0)

if __name__ == '__main__':
    unittest.main()
