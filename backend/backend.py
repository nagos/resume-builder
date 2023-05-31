from mysql.connector import connect, Error
from passlib.hash import sha256_crypt

class BackendError(Exception):
    pass

class Backend():
    def __init__(self, db_server, db_name):
        self.db_server = db_server
        self.db_name = db_name
    
    def get_db(self):
        cnx = connect(
                host = self.db_server,
                user = "root",
                password = "",
                database = self.db_name
            )
        cursor = cnx.cursor()
        return cnx, cursor
    
    def hash_password(self, password):
        return sha256_crypt.hash(password)

    def check_password(self, password, hash):
        return sha256_crypt.verify(password, hash)

    def db_query(self, query, data = None):
        try:
            cnx, cursor = self.get_db()
        except Error as err:
            raise BackendError(f'Database error: {err}')

        try:
            cursor.execute(query, data)
            rowid = cursor.lastrowid
            rowcount = cursor.rowcount
            row = cursor.fetchall()
        except Error as err:
            raise BackendError(f'Database error: {err}')
        finally:
            cnx.commit()
            cnx.close()
        
        return row, rowid, rowcount

    def user_register(self, user, password):
        password_hash = self.hash_password(password)
        create_user_query = "INSERT INTO users (login, password) VALUES (%s, %s)"
        row, rowid, rowcount = self.db_query(create_user_query, (user, password_hash))
        return rowid
    
    def user_login(self, user, password):
        user_password_query = "SELECT id, password FROM users WHERE login=%s"
        row, rowid, rowcount = self.db_query(user_password_query, (user,))
        if row:
            user_id, password_hash = row[0]
        else:
            user_id, password_hash = None, None
        
        if self.check_password(password, password_hash):
            return user_id
        else:
            return None
    
    def resume_list(self, user_id):
        resume_get_query = "SELECT id FROM resume WHERE user_id=%s"
        row, rowid, rowcount = self.db_query(resume_get_query, (user_id,))
        return [id for (id,) in row]

    def resume_get(self, id):
        resume_get_query = "SELECT text FROM resume WHERE id=%s"
        row, rowid, rowcount = self.db_query(resume_get_query, (id,))
        if row:
            return row[0][0]
        else:
            return None
    
    def resume_create(self, user_id, text):
        resume_get_query = "INSERT INTO resume (user_id, text) VALUES (%s, %s)"
        row, rowid, rowcount = self.db_query(resume_get_query, (user_id, text))

    def resume_update(self, user_id, id, text):
        resume_update_query = "UPDATE resume SET text=%s WHERE id=%s and user_id=%s"
        row, rowid, rowcount = self.db_query(resume_update_query, (text, id, user_id))
        if rowcount == 1:
            return True
        else:
            return False
    
    def resume_delete(self, user_id, id):
        resume_delete_query = "DELETE FROM resume WHERE id=%s and user_id=%s"
        row, rowid, rowcount = self.db_query(resume_delete_query, (id, user_id))
        if rowcount == 1:
            return True
        else:
            return False