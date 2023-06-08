from flask import Flask
import os
from flask_login import LoginManager
from flask_restful import Api

from resume_api import ResumeListApi, ResumeApi
from user_api import UserApi
from backend import Backend
from db_models import db

app = Flask(__name__)
app.secret_key = os.getenv('API_KEY', 'dev key')
api = Api(app)
db_server = os.getenv('DB_SERVER', "localhost")
db_name = "resume"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:@{db_server}/{db_name}"

db.init_app(app)

backend = Backend()
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return backend.get_user(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return {'login': False}, 401

api.add_resource(ResumeListApi, '/api/resume/')
api.add_resource(ResumeApi, '/api/resume/<int:id>/<string:fmt>', '/api/resume/<int:id>')
api.add_resource(UserApi, '/api/user')
