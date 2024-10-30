from flask import Flask
from config import app, db
from routes.aluno_routes import alunos_bp
from routes.professor_routes import professores_bp
from routes.turma_routes import turmas_bp

app.register_blueprint(alunos_bp, url_prefix='/api')
app.register_blueprint(professores_bp, url_prefix='/api')
app.register_blueprint(turmas_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])

