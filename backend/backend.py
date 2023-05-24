from mysql.connector import connect, Error

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
