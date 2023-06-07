from flask_restful import Resource
from flask_login import current_user, login_user, logout_user
from flask import request, current_app as app

from backend import Backend, BackendError

class UserApi(Resource):
    def __init__(self):
        self.backend = Backend.get()

    def get(self):
        """Login status"""
        if current_user.is_authenticated:
            return {'login': True}
        else:
            return {'login': False}
    
    def post(self):
        """User login"""
        user = request.json.get('user')
        password = request.json.get('password')
        if user is None or password is None:
            return {'login': False}, 400
        try:
            user_id = self.backend.user_login(user, password)
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'login': False}, 400

        if user_id is not None:
            user_object = self.backend.get_user(user_id)
            login_user(user_object, remember=True)
            return {'login': True}
        else:
            return {'login': False}, 400
    
    def put(self):
        """User register"""
        user = request.json.get('user')
        password = request.json.get('password')
        if user is None or password is None:
            return {'login': False}, 400
        try:
            user_id = self.backend.user_register(user, password)
        except BackendError as err:
            app.logger.error(err)
            return {'login': False}, 400

        user_object = self.backend.get_user(user_id)
        login_user(user_object, remember=True)

        return {'login': True}

    def delete(self):
        """User logout"""
        logout_user()
        return {'login': False}
