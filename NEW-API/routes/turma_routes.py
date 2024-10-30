from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.turma import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template("/turmas/turmas.html", turmas=turmas)


@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('/turmas/turma_id.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_bp.route('/turmas/criar', methods=['GET'])
def adicionar_turma_page():
    return render_template('/turmas/criar_turma.html')


@turmas_bp.route('/turmas', methods=['POST'])
def create_turma():
    nova_turma = {
        'descricao': request.form['descricao'],
        'ativo': request.form.get('ativo') == 'on',
        'professor_id': int(request.form['professor_id'])
    }
    adicionar_turma(nova_turma)
    return redirect(url_for('turmas.get_turmas'))


@turmas_bp.route('/turmas/atualizar/<int:id_turma>', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('/turmas/turma_update.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_bp.route('/turmas/<int:id_turma>', methods=['POST'])
def update_turma(id_turma):
    novos_dados = {
        'descricao': request.form['descricao'],
        'ativo': request.form.get('ativo') == 'on',
        'professor_id': int(request.form['professor_id'])
    }
    try:
        atualizar_turma(id_turma, novos_dados)
        return redirect(url_for('turmas.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_bp.route('/turmas/<int:id_turma>/delete', methods=['POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
