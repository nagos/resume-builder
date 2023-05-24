from flask import Flask, request, session, g
import os
from mysql.connector import connect, Error

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
db_server = os.getenv('DB_SERVER')

def get_db():
    cnx = connect(
            host=db_server,
            user="root",
            password="",
            database="resume"
        )
    cursor = cnx.cursor()
    return cnx, cursor

@app.route('/api/login/register', methods=['POST'])
def register():
    cnx, cursor = get_db()
    try:
        create_user_query = "INSERT INTO users (login, password) VALUES (%s, %s)"
        user = request.form.get('user')
        password = request.form.get('password')
        cursor.execute(create_user_query, (user, password))
        session['login'] = True
        session['id'] = cursor.lastrowid
    except:
        return "fail", 400
    cnx.commit()
    cnx.close()
    return "ok"

@app.route('/api/login/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    cnx, cursor = get_db()
    user_password_query = "SELECT id, password FROM users WHERE login=%s"
    cursor.execute(user_password_query, (user,))
    user_id, user_password = cursor.fetchone()
    if password == user_password:
        session['login'] = True
        session['id'] = user_id
    else:
        return "fail", 400
    cnx.close()
    return "ok"

@app.route('/api/login/logout', methods=['POST'])
def logout():
    session.clear()
    return "ok"

@app.route('/api/resume/<int:id>')
def resume_get(id):
    cnx, cursor = get_db()
    try:
        resume_get_query = "SELECT text FROM resume WHERE id=%s"
        cursor.execute(resume_get_query, (id,))
        text, = cursor.fetchone()
    except:
        return "fail", 400
    cnx.close()
    return text

@app.route('/api/resume/')
def resume_list():
    if not session.get('login'):
        return "fail", 400
    cnx, cursor = get_db()
    ret = []
    user_id = session.get('id')
    try:
        resume_get_query = "SELECT id FROM resume WHERE user_id=%s"
        cursor.execute(resume_get_query, (user_id,))
        for id, in cursor.fetchall():
            ret.append(id)
    except:
        return "fail", 400
    cnx.close()
    return ret

@app.route('/api/resume/create', methods=['POST'])
def resume_create():
    if not session.get('login'):
        return "fail", 400
    text = request.form.get('text')
    cnx, cursor = get_db()
    user_id = session.get('id')
    try:
        resume_get_query = "INSERT INTO resume (user_id, text) VALUES (%s, %s)"
        cursor.execute(resume_get_query, (user_id, text))
        cnx.commit()
    except:
        return "fail", 400
    cnx.close()
    return "ok"

@app.route('/api/resume/<int:id>/update', methods=['POST'])
def resume_update(id):
    if not session.get('login'):
        return "fail", 400
    text = request.form.get('text')
    cnx, cursor = get_db()
    user_id = session.get('id')
    try:
        resume_update_query = "UPDATE resume SET text=%s WHERE id=%s and user_id=%s"
        cursor.execute(resume_update_query, (text, id, user_id))
        cnx.commit()
    except:
        return "fail", 400
    if cursor.rowcount != 1:
        return "fail", 400
    cnx.close()
    return "ok"


@app.route('/api/resume/<int:id>/delete', methods=['POST'])
def resume_delete(id):
    if not session.get('login'):
        return "fail", 400
    cnx, cursor = get_db()
    user_id = session.get('id')
    try:
        resume_update_query = "DELETE FROM resume WHERE id=%s and user_id=%s"
        cursor.execute(resume_update_query, (id, user_id))
        cnx.commit()
    except:
        return "fail", 400
    if cursor.rowcount != 1:
        return "fail", 400
    cnx.close()
    return "ok"
