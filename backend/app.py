from flask import Flask, request
import os
from flask_login import LoginManager
from flask_restful import Api
from resume_api import ResumeListApi, ResumeApi
from user_api import UserApi
from backend import Backend

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
api = Api(app)
db_server = os.getenv('DB_SERVER')

backend = Backend(db_server, "resume")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return backend.get_user(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return {'login': False}, 401

api.add_resource(ResumeListApi, '/api/resume/')
api.add_resource(ResumeApi, '/api/resume/<int:id>/<string:fmt>', '/api/resume/<int:id>')
api.add_resource(UserApi, '/api/user')
