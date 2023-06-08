from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from user import UserSession
from sqlalchemy.exc import DatabaseError

from db_models import db, User, Resume;

class BackendError(Exception):
    pass

class Backend():
    instance = None
    def get():
        return Backend.instance

    def __init__(self):
        Backend.instance = self
    
    def get_user(self, user_id):
        return UserSession(user_id)
    
    def hash_password(self, password):
        return sha256_crypt.hash(password)

    def check_password(self, password, hash):
        return sha256_crypt.verify(password, hash)

    def user_register(self, user, password):
        password_hash = self.hash_password(password)
        user = User(login=user, password=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')

        return user.id
    
    def user_login(self, user, password):
        try:
            user = db.session.execute(db.select(User).where(User.login==user)).scalar()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')

        if user is None:
            return None
        
        if self.check_password(password, user.password):
            return user.id
        else:
            return None
    
    def resume_list(self, user_id):
        try:
            resumes = db.session.execute(db.select(Resume).where(Resume.user_id==user_id)).scalars()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')
        return [{'id': resume.id, 'title': resume.title} for resume in resumes]

    def resume_get(self, id):
        try:
            resume = db.session.execute(db.select(Resume).where(Resume.id==id)).scalar()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')
        if resume:
            return resume.title, resume.text
        else:
            return None, None
    
    def resume_create(self, user_id, title, text):
        resume = Resume(user_id=user_id, title=title, text=text)
        try:
            db.session.add(resume)
            db.session.commit()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')

    def resume_update(self, user_id, id, title, text):
        try:
            result = db.session.execute(db.update(Resume)
                .where(Resume.id==id).where(Resume.user_id==user_id)
                .values({"title":title, "text": text })
            )
            db.session.commit()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')

        if result.rowcount == 1:
            return True
        else:
            return False
    
    def resume_delete(self, user_id, id):
        try:
            result = db.session.execute(db.delete(Resume)
                .where(Resume.id==id).where(Resume.user_id==user_id)
            )
            db.session.commit()
        except DatabaseError as err:
            raise BackendError(f'Database error: {err}')
        
        if result.rowcount == 1:
            return True
        else:
            return False
