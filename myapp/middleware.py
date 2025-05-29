import threading

_user = threading.local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before view: store request.user on thread‑local
        _user.value = request.user
        response = self.get_response(request)
        # after view: (optional) clear it if you like
        return response

def get_current_user():
    return getattr(_user, "value", None)

