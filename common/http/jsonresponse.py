from django.utils import simplejson
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data):
        self.set_content(data)
        super(JsonResponse, self).__init__(content=self.get_content,
                                           mimetype='application/json')
    def set_content(self, content):
        self.content = content
    def get_content(self, json_encoded=True):
        if json_encoded:
            return simplejson.dumps(self.content)
        else:
            return self.content

class Success(JsonResponse):
    def __init__(self, data):
        x = data
        content = { 'type': 'success', 'data': x}
        super(Success, self).__init__(content)


class Failure(JsonResponse):
    def __init__(self, data):
        x = data
        content = { 'type': 'error', 'data': x}
        super(Failure, self).__init__(content)

class AuthFailure(Failure)
    def __init__(self, message, code=1):
        x = { 'message': message, 'code': code }
        super(AuthFailure, self).__init__(data)

class AuthSucces(Success)
    def __init__(self, session_key):
        x = { 'session_key': session_key }
        super(AuthFailure, self).__init__(data)