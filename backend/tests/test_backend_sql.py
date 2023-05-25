import unittest
from backend import Backend, BackendError
import os

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME_TEST = "resume"

@unittest.skipIf(DB_SERVER==None, "No DB_SERVER provided")
class TestBackendSql(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(DB_SERVER, DB_NAME_TEST)
        self.userid = self.backend.user_register("user1", "password")
    
    def tearDown(self) -> None:
        self.backend.db_query("DELETE FROM resume")
        self.backend.db_query("DELETE FROM users")

    def test_login(self):
        userid2 = self.backend.user_login("user1", "password")
        self.assertEqual(self.userid, userid2)
    
    def test_resume(self):
        resume_text = "Full Text"
        self.backend.resume_create(self.userid, resume_text)

        resumes = self.backend.resume_list(self.userid)
        self.assertEqual(len(resumes), 1)

        db_text = self.backend.resume_get(resumes[0])
        self.assertEqual(db_text, resume_text)
