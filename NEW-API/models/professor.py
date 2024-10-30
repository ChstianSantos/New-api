from config import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(200))

    turmas = db.relationship('Turma', back_populates='professor', cascade="all, delete-orphan")

    def __init__(self, nome, idade, materia, observacoes=None):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes,
            'turmas': [{'id': turma.id, 'descricao': turma.descricao} for turma in self.turmas]
        }


class ProfessorNaoEncontrado(Exception):
    pass

def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()

def adicionar_professor(professor_data):
    novo_professor = Professor(
        nome=professor_data['nome'],
        idade=int(professor_data['idade']),
        materia=professor_data['materia'],
        observacoes=professor_data.get('observacoes')
    )
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado

    professor.nome = novos_dados['nome']
    professor.idade = int(novos_dados['idade'])
    professor.materia = novos_dados['materia']
    professor.observacoes = novos_dados.get('observacoes')
    
    db.session.commit()

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado

    db.session.delete(professor)
    db.session.commit()
