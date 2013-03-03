from django.utils import simplejson
from django.http import HttpResponse

class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = simplejson.dumps(data)
        super(JsonResponse, self).__init__(content=content,
                                           mimetype='application/json')

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