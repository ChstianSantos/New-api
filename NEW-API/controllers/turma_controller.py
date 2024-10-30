from flask import request, jsonify
from models.turma import Turma, adicionar_turma, listar_turmas, turma_por_id, atualizar_turma, excluir_turma, TurmaNaoEncontrada

def create_turma():
    data = request.get_json()
    adicionar_turma(data)
    return jsonify({'message': 'Turma criada com sucesso!'}), 201

def get_turmas():
    turmas = listar_turmas()
    return jsonify(turmas), 200

def get_turma(turma_id):
    try:
        turma = turma_por_id(turma_id)
        return jsonify(turma), 200
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada!'}), 404

def update_turma(turma_id):
    data = request.get_json()
    try:
        atualizar_turma(turma_id, data)
        return jsonify({'message': 'Turma atualizada com sucesso!'}), 200
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada!'}), 404

def delete_turma(turma_id):
    try:
        excluir_turma(turma_id)
        return jsonify({'message': 'Turma deletada com sucesso!'}), 200
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada!'}), 404
