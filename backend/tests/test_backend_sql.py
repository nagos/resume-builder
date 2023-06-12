import unittest
from backend import Backend, BackendError, NotFoundError
import os
from db_models import db
from flask import Flask

db_server = os.getenv('DB_SERVER')
db_name = "resume"

@unittest.skipIf(db_server==None, "No DB_SERVER provided")
class TestBackendSql(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:@{db_server}/{db_name}"
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()
            cls.backend = Backend()
            cls.userid = cls.backend.user_register("user1", "password")
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.backend.user_delete("user1")

    def test_login(self):
        with self.app.app_context():
            userid2 = TestBackendSql.backend.user_login("user1", "password")
            self.assertEqual(self.userid, userid2)
    
    def test_resume(self):
        with self.app.app_context():
            resume_title = "Title"
            resume_text = "Full Text"
            self.backend.resume_create(self.userid, resume_title, resume_text)

            resumes = self.backend.resume_list(self.userid)
            self.assertEqual(len(resumes), 1)

            db_text = self.backend.resume_get(resumes[0]['id'])
            self.assertEqual(db_text, (resume_title, resume_text))

            self.backend.resume_delete(self.userid, resumes[0]['id'])

    def test_non_existing_delete(self):
        with self.app.app_context():
            with self.assertRaises(NotFoundError):
                self.backend.resume_delete(self.userid, 9999)

    def test_wrong_user_delete(self):
        with self.app.app_context():
            resume_title = "Title"
            resume_text = "Full Text"
            self.backend.resume_create(self.userid, resume_title, resume_text)
            resumes = self.backend.resume_list(self.userid)
            with self.assertRaises(BackendError):
                self.backend.resume_delete(9999, resumes[0]['id'])
            self.backend.resume_delete(self.userid, resumes[0]['id'])

    def test_non_existing_update(self):
        with self.app.app_context():
            with self.assertRaises(NotFoundError):
                self.backend.resume_update(self.userid, 9999, "title", "text")

    def test_non_existing_get(self):
        with self.app.app_context():
            with self.assertRaises(NotFoundError):
                self.backend.resume_get(9999)
