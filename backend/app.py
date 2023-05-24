from flask import Flask, request, session
import os
from mysql.connector import connect

from backend import Backend, BackendError

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
db_server = os.getenv('DB_SERVER')

backend = Backend(db_server, "resume")

@app.route('/api/login/register', methods=['POST'])
def register():
    create_user_query = "INSERT INTO users (login, password) VALUES (%s, %s)"
    user = request.form.get('user')
    password = request.form.get('password')
        
    try:
        row, rowid, rowcount = backend.db_query(create_user_query, (user, password))
    except BackendError as err:
        app.logger.error(err)
        return "fail", 400

    session['login'] = True
    session['id'] = rowid

    return "ok"

@app.route('/api/login/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    user_password_query = "SELECT id, password FROM users WHERE login=%s"
    try:
        row, rowid, rowcount = backend.db_query(user_password_query, (user,))
        if row:
            user_id, user_password = row[0]
        else:
            user_id, user_password = None, None
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400

    if password == user_password:
        session['login'] = True
        session['id'] = user_id
        return "ok"
    else:
        return "fail", 400

@app.route('/api/login/logout', methods=['POST'])
def logout():
    session.clear()
    return "ok"

@app.route('/api/resume/<int:id>')
def resume_get(id):
    resume_get_query = "SELECT text FROM resume WHERE id=%s"
    try:
        row, rowid, rowcount = backend.db_query(resume_get_query, (id,))
        if row:
            text, = row[0]
        else:
            return "fail", 400
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    return text

@app.route('/api/resume/')
def resume_list():
    if not session.get('login'):
        return "fail", 400
    ret = []
    user_id = session.get('id')
    resume_get_query = "SELECT id FROM resume WHERE user_id=%s"
    try:
        row, rowid, rowcount = backend.db_query(resume_get_query, (user_id,))
        for id, in row:
            ret.append(id)
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    return ret

@app.route('/api/resume/create', methods=['POST'])
def resume_create():
    if not session.get('login'):
        return "fail", 400
    text = request.form.get('text')
    user_id = session.get('id')
    resume_get_query = "INSERT INTO resume (user_id, text) VALUES (%s, %s)"
    try:
        row, rowid, rowcount = backend.db_query(resume_get_query, (user_id, text))
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    return "ok"

@app.route('/api/resume/<int:id>/update', methods=['POST'])
def resume_update(id):
    if not session.get('login'):
        return "fail", 400
    text = request.form.get('text')
    user_id = session.get('id')
    resume_update_query = "UPDATE resume SET text=%s WHERE id=%s and user_id=%s"
    try:
        row, rowid, rowcount = backend.db_query(resume_update_query, (text, id, user_id))
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    if rowcount != 1:
        return "fail", 400
    return "ok"

@app.route('/api/resume/<int:id>/delete', methods=['POST'])
def resume_delete(id):
    if not session.get('login'):
        return "fail", 400
    user_id = session.get('id')
    resume_delete_query = "DELETE FROM resume WHERE id=%s and user_id=%s"
    try:
        row, rowid, rowcount = backend.db_query(resume_delete_query, (id, user_id))
    except BackendError as err:
        app.logger.error(f'Backend error: {err}')
        return "fail", 400
    if rowcount != 1:
        return "fail", 400
    return "ok"
