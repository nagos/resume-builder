from flask_restful import Resource
from flask_login import current_user, login_required
from flask import request, Response, current_app as app
import markdown

from backend import Backend, BackendError, NotFoundError

class ResumeListApi(Resource):
    def __init__(self):
        self.backend = Backend()

    @login_required
    def get(self):
        """Read list"""
        user_id = current_user.get_id_int()
        try:
            ids = self.backend.resume_list(user_id)
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 400
        return ids
    
    @login_required
    def post(self):
        """Create resume"""
        title = request.json.get('title')
        text = request.json.get('text')
        user_id = current_user.get_id_int()
        try:
            self.backend.resume_create(user_id, title, text)
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 400
        return {'status': 'ok'}

class ResumeApi(Resource):
    def __init__(self):
        self.backend = Backend()

    def get(self, id, fmt=None):
        """Read resume"""
        try:
            title, text = self.backend.resume_get(id)
        except NotFoundError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 404
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 400

        if fmt == 'html':
            return Response(markdown.markdown(text), mimetype='text/hmll')
        else:
            return {'text': text, 'title': title}
    
    @login_required
    def put(self, id, fmt=None):
        """Update resume"""
        title = request.json.get('title')
        text = request.json.get('text')
        user_id = current_user.get_id_int()
        
        try:
            self.backend.resume_update(user_id, id, title, text)
        except NotFoundError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 404
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 400

        return {'status': 'ok'}
        
    @login_required
    def delete(self, id, fmt=None):
        """Delete resume"""
        user_id = current_user.get_id_int()
        try:
            self.backend.resume_delete(user_id, id)
        except NotFoundError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 404
        except BackendError as err:
            app.logger.error(f'Backend error: {err}')
            return {'status': 'error'}, 400

        return {'status': 'ok'}
