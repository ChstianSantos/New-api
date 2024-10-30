from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.aluno import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_bp = Blueprint('alunos', __name__)


# mostrar
@alunos_bp.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("/alunos/alunos.html", alunos=alunos)

# mostrar por id
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('/alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# criar
@alunos_bp.route('/alunos/criar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('/alunos/criar_aluno.html')

@alunos_bp.route('/alunos', methods=['POST'])
def create_aluno():
    novo_aluno = {
        'nome': request.form['nome'],
        'idade': int(request.form['idade']),
        'data_nascimento': request.form['data_nascimento'],
        'nota_primeiro_semestre': float(request.form['nota_primeiro_semestre']),
        'nota_segundo_semestre': float(request.form['nota_segundo_semestre']),
        'media_final': float(request.form['media_final']),
        'turma_id': int(request.form['turma_id'])  
    }
    adicionar_aluno(novo_aluno)
    return redirect(url_for('alunos.get_alunos'))

@alunos_bp.route('/alunos/atualizar/<int:id_aluno>', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('/alunos/aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['POST'])
def update_aluno(id_aluno):
    novos_dados = {
        'nome': request.form['nome'],
        'idade': int(request.form['idade']),
        'data_nascimento': request.form['data_nascimento'],
        'nota_primeiro_semestre': float(request.form['nota_primeiro_semestre']),
        'nota_segundo_semestre': float(request.form['nota_segundo_semestre']),
        'media_final': float(request.form['media_final']),
        'turma_id': int(request.form['turma_id']) 
    }
    try:
        atualizar_aluno(id_aluno, novos_dados)
        return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_bp.route('/alunos/delete/<int:id_aluno>', methods=['POST'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

