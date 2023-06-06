from flask import Flask, request
import flask
import os
from mysql.connector import connect
import markdown
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from backend import Backend, BackendError

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
db_server = os.getenv('DB_SERVER')

backend = Backend(db_server, "resume")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return backend.get_user(user_id)

@app.route('/api/user/register', methods=['POST'])
def user_register():
    user = request.json.get('user')
    password = request.json.get('password')
    if user is None or password is None:
        return {'login': False}, 400
    try:
        user_id = backend.user_register(user, password)
    except BackendError as err:
        app.logger.error(err)
        return {'login': False}, 400

    user_object = backend.get_user(user_id)
    login_user(user_object, remember=True)

    return {'login': True}

@app.route('/api/user/status')
def user_status():
    if current_user.is_authenticated:
        return {'login': True}
    else:
        return {'login': False}

@app.route('/api/user/login', methods=['POST'])
def user_login():
    user = request.json.get('user')
    password = request.json.get('password')
    if user is None or password is None:
        return {'login': False}, 400
    try:
        user_id = backend.user_login(user, password)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'login': False}, 400

    if user_id is not None:
        user_object = backend.get_user(user_id)
        login_user(user_object, remember=True)
        return {'login': True}
    else:
        return {'login': False}, 400

@app.route('/api/user/logout', methods=['POST'])
def user_logout():
    logout_user()
    return {'login': False}

@app.route('/api/resume/<int:id>/<string:fmt>')
def resume_get(id, fmt):
    try:
        title, text = backend.resume_get(id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'status': 'error'}, 400

    if text is None:
        return {'status': 'error'}, 400
    if fmt == 'html':
        return markdown.markdown(text)
    else:
        return {'text': text, 'title': title}

@app.route('/api/resume/')
@login_required
def resume_list():
    user_id = current_user.get_id_int()
    try:
        ids = backend.resume_list(user_id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'status': 'error'}, 400
    return ids

@app.route('/api/resume/create', methods=['POST'])
@login_required
def resume_create():
    title = request.json.get('title')
    text = request.json.get('text')
    user_id = current_user.get_id_int()
    try:
        backend.resume_create(user_id, title, text)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'status': 'error'}, 400
    return {'status': 'ok'}

@app.route('/api/resume/<int:id>/update', methods=['POST'])
@login_required
def resume_update(id):
    title = request.json.get('title')
    text = request.json.get('text')
    user_id = current_user.get_id_int()
    
    try:
        ret = backend.resume_update(user_id, id, title, text)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'status': 'error'}, 400

    if ret:
        return {'status': 'ok'}
    else:
        return {'status': 'error'}, 400

@app.route('/api/resume/<int:id>/delete', methods=['POST'])
@login_required
def resume_delete(id):
    user_id = current_user.get_id_int()
    try:
        ret = backend.resume_delete(user_id, id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return {'status': 'error'}, 400

    if ret:
        return {'status': 'ok'}
    else:
        return {'status': 'error'}, 400

@login_manager.unauthorized_handler
def unauthorized():
    return {'login': False}, 401
