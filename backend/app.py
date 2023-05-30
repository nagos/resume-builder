from flask import Flask, request
import flask
import os
from mysql.connector import connect
import markdown

from backend import Backend, BackendError
from sessionManager import sessionManager

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
db_server = os.getenv('DB_SERVER')

backend = Backend(db_server, "resume")
session = sessionManager(flask.session)

@app.route('/api/user/register', methods=['POST'])
def register():
    user = request.form.get('user')
    password = request.form.get('password')
        
    try:
        user_id = backend.user_register(user, password)
    except BackendError as err:
        app.logger.error(err)
        return "fail", 400

    session.login(user_id)

    return "ok"

@app.route('/api/user/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    try:
        user_id = backend.user_login(user, password)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400

    if not user_id is None:
        session.login(user_id)
        return "ok"
    else:
        return "fail", 400

@app.route('/api/user/logout', methods=['POST'])
def logout():
    session.logout()
    return "ok"

@app.route('/api/resume/<int:id>/<string:fmt>')
def resume_get(id, fmt):
    try:
        text = backend.resume_get(id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400

    if text is None:
        return "fail", 400
    if fmt == 'html':
        return markdown.markdown(text)
    else:
        return text

@app.route('/api/resume/')
def resume_list():
    if not session.is_login():
        return "fail", 400
    user_id = session.user_id()
    try:
        ids = backend.resume_list(user_id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    if len(ids):
        return ids
    else:
        return "fail", 400

@app.route('/api/resume/create', methods=['POST'])
def resume_create():
    if not session.is_login():
        return "fail", 400
    text = request.form.get('text')
    user_id = session.user_id()
    try:
        backend.resume_create(user_id, text)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    return "ok"

@app.route('/api/resume/<int:id>/update', methods=['POST'])
def resume_update(id):
    if not session.is_login():
        return "fail", 400
    text = request.form.get('text')
    user_id = session.user_id()
    
    try:
        ret = backend.resume_update(user_id, id, text)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400

    if ret:
        return "ok"
    else:
        return "fail", 400

@app.route('/api/resume/<int:id>/delete', methods=['POST'])
def resume_delete(id):
    if not session.is_login():
        return "fail", 400
    user_id = session.user_id()
    try:
        ret = backend.resume_delete(user_id, id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400

    if ret:
        return "ok"
    else:
        return "fail", 400
