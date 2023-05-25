class sessionManager():
    def __init__(self, session):
        self.session = session
        pass

    def login(self, userid):
        self.session['login'] = True
        self.session['id'] = userid
    
    def logout(self):
        self.session.clear()
    
    def is_login(self):
        if self.session.get('login'):
            return True
        else:
            return False
    
    def user_id(self):
        return self.session.get('id')
