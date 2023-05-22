from flask import Flask, request, session, g
import os
from mysql.connector import connect, Error

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
db_server = os.getenv('DB_SERVER')

def get_db_connection():
    cnx = getattr(g, '_database', None)
    if cnx is None:
        cnx = g._database = connect(
            host=db_server,
            user="root",
            password="",
            database="resume"
        )
    return cnx

@app.route('/api/login/register', methods=['POST'])
def register():
    cnx = get_db_connection()
    try:
        with cnx.cursor() as cursor:
            create_user_query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            user = request.form.get('user')
            password = request.form.get('password')
            cursor.execute(create_user_query, (user, password))
            session['login'] = True
            print(user, password)
            cnx.commit()
    except:
        return "fail", 400
    return "ok"

@app.route('/api/login/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    cnx = get_db_connection()
    with cnx.cursor() as cursor:
        user_password_query = "SELECT id, password FROM users WHERE login=%s"
        cursor.execute(user_password_query, (user,))
        user_id, user_password = cursor.fetchone()
        if password == user_password:
            session['login'] = True
            session['id'] = user_id
        else:
            return "fail", 400
    return "ok"

@app.route('/api/login/logout', methods=['POST'])
def logout():
    session.clear()
    return "ok"
