import threading

thread_locals = threading.local()


class RequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals.request = request

        response = self.get_response(request)

        del thread_locals.request

        return response


