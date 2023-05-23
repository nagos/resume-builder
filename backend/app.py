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
