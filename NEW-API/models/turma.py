from config import db
from sqlalchemy.orm import joinedload

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professor', back_populates='turmas')

    alunos = db.relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome if self.professor else None
        }


class TurmaNaoEncontrada(Exception):
    pass

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def turma_por_id(id_turma):
    turma = Turma.query.options(joinedload(Turma.professor)).get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma

def adicionar_turma(turma_data):
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        ativo=turma_data['ativo'],
        professor_id=turma_data['professor_id']
    )
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada

    turma.descricao = novos_dados['descricao']
    turma.ativo = novos_dados['ativo']
    turma.professor_id = novos_dados['professor_id']

    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada

    db.session.delete(turma)
    db.session.commit()
