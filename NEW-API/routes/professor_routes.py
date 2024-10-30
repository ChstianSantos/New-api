from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.professor import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template("/professores/professores.html", professores=professores)

@professores_bp.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('/professores/professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_bp.route('/professores/criar', methods=['GET'])
def adicionar_professor_page():
    return render_template('/professores/criar_professor.html')

@professores_bp.route('/professores', methods=['POST'])
def create_professor():
    novo_professor = {
        'nome': request.form['nome'],
        'idade': request.form['idade'],
        'materia': request.form['materia'],
        'observacoes': request.form.get('observacoes')
    }
    adicionar_professor(novo_professor)
    return redirect(url_for('professores.get_professores'))

@professores_bp.route('/professores/atualizar/<int:id_professor>', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('/professores/professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_bp.route('/professores/<int:id_professor>', methods=['POST'])
def update_professor(id_professor):
    novos_dados = {
        'nome': request.form['nome'],
        'idade': request.form['idade'],
        'materia': request.form['materia'],
        'observacoes': request.form.get('observacoes')
    }
    try:
        atualizar_professor(id_professor, novos_dados)
        return redirect(url_for('professores.get_professor', id_professor=id_professor))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_bp.route('/professores/delete/<int:id_professor>', methods=['POST'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return redirect(url_for('professores.get_professores'))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
