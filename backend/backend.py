from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from user import User
from sqlalchemy import text
from sqlalchemy.exc import DatabaseError

class BackendError(Exception):
    pass

class Backend():
    instance = None
    def get():
        return Backend.instance

    def __init__(self, db_server, db_name):
        self.db_server = db_server
        self.db_name = db_name
        self.engine = create_engine(f"mysql+pymysql://root:@{db_server}/{db_name}")
        Backend.instance = self
    
    def get_user(self, user_id):
        return User(user_id)
    
    def hash_password(self, password):
        return sha256_crypt.hash(password)

    def check_password(self, password, hash):
        return sha256_crypt.verify(password, hash)

    def db_query(self, query, data = None, fetch=False):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), [data])
                rowid = result.lastrowid
                rowcount = result.rowcount
                if fetch:
                    row = result.all()
                else:
                    row = []
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')
        
        return row, rowid, rowcount

    def user_register(self, user, password):
        password_hash = self.hash_password(password)
        create_user_query = "INSERT INTO users (login, password) VALUES (:login, :password)"
        row, rowid, rowcount = self.db_query(create_user_query, {"login": user, "password": password_hash})
        return rowid
    
    def user_login(self, user, password):
        user_password_query = "SELECT id, password FROM users WHERE login=:login"
        row, rowid, rowcount = self.db_query(user_password_query, {"login":user}, fetch=True)
        if row:
            user_id, password_hash = row[0]
        else:
            return None
        
        if self.check_password(password, password_hash):
            return user_id
        else:
            return None
    
    def resume_list(self, user_id):
        resume_get_query = "SELECT id, title FROM resume WHERE user_id=:user_id"
        row, rowid, rowcount = self.db_query(resume_get_query, {"user_id": user_id}, fetch=True)
        return [{'id': id, 'title': title} for (id, title) in row]

    def resume_get(self, id):
        resume_get_query = "SELECT title, text FROM resume WHERE id=:id"
        row, rowid, rowcount = self.db_query(resume_get_query, {"id": id}, fetch=True)
        if row:
            return row[0][0:2]
        else:
            return None, None
    
    def resume_create(self, user_id, title, text):
        resume_get_query = "INSERT INTO resume (user_id, title, text) VALUES (:user_id, :title, :text)"
        row, rowid, rowcount = self.db_query(resume_get_query, {"user_id": user_id, "title": title, "text": text})

    def resume_update(self, user_id, id, title, text):
        resume_update_query = "UPDATE resume SET title=:title, text=:text WHERE id=:id and user_id=:user_id"
        row, rowid, rowcount = self.db_query(resume_update_query, {"title": title, "text": text, "id": id, "user_id": user_id})
        if rowcount == 1:
            return True
        else:
            return False
    
    def resume_delete(self, user_id, id):
        resume_delete_query = "DELETE FROM resume WHERE id=:id and user_id=:user_id"
        row, rowid, rowcount = self.db_query(resume_delete_query, {"id": id, "user_id": user_id})
        if rowcount == 1:
            return True
        else:
            return False
