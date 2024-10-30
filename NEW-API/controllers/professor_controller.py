from flask import request, jsonify
from models.professor import adicionar_professor, listar_professores, professor_por_id, atualizar_professor, excluir_professor, ProfessorNaoEncontrado

def create_professor():
    data = request.get_json()
    adicionar_professor(data)
    return jsonify({'message': 'Professor criado com sucesso!'}), 201

def get_professores():
    professores = listar_professores()
    return jsonify(professores), 200

def get_professor(professor_id):
    try:
        professor = professor_por_id(professor_id)
        return jsonify(professor), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado!'}), 404

def update_professor(professor_id):
    data = request.get_json()
    try:
        atualizar_professor(professor_id, data)
        return jsonify({'message': 'Professor atualizado com sucesso!'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado!'}), 404

def delete_professor(professor_id):
    try:
        excluir_professor(professor_id)
        return jsonify({'message': 'Professor deletado com sucesso!'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado!'}), 404
