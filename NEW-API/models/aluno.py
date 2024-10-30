from config import db
from datetime import datetime

# criação da tabela de banco de dados
class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=True)

    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    turma = db.relationship('Turma', back_populates='alunos')

    def __init__(self, nome, idade, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
        self.turma_id = turma_id

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'turma': self.turma.to_dict() if self.turma else None
    }

# criação de funções, para uso
class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(aluno_data):
    data_nascimento = datetime.strptime(aluno_data['data_nascimento'], '%Y-%m-%d').date()
    novo_aluno = Aluno(
        nome=aluno_data['nome'],
        idade=int(aluno_data['idade']),
        data_nascimento=data_nascimento,
        nota_primeiro_semestre=float(aluno_data['nota_primeiro_semestre']),
        nota_segundo_semestre=float(aluno_data['nota_segundo_semestre']),
        turma_id=aluno_data['turma_id']
    )
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado

    aluno.nome = novos_dados['nome']
    aluno.idade = int(novos_dados['idade'])
    aluno.data_nascimento = datetime.strptime(novos_dados['data_nascimento'], '%Y-%m-%d').date()
    aluno.nota_primeiro_semestre = float(novos_dados['nota_primeiro_semestre'])
    aluno.nota_segundo_semestre = float(novos_dados['nota_segundo_semestre'])
    aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
    aluno.turma_id = int(novos_dados['turma_id'])

    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado

    db.session.delete(aluno)
    db.session.commit()
