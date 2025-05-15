from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ImproperlyConfigured

class SessionHistoryMiddleware(MiddlewareMixin):
    """
    Stores a limited navigation history in `request.session['history']`.

    - Tracks only safe GET requests (non-AJAX)
    - Skips duplicates to avoid noise
    - Configurable max length via `SESSION_HISTORY_MAX_LENGTH`
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        max_len = getattr(settings, 'SESSION_HISTORY_MAX_LENGTH', None)
        if max_len is None or not isinstance(max_len, int) or max_len < 1:
            raise ImproperlyConfigured(
                "`SESSION_HISTORY_MAX_LENGTH` must be a positive integer in settings."
            )
        self.max_len = max_len

    def process_request(self, request):
        # Only track GET requests without AJAX header
        if request.method != 'GET' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return None

        history = request.session.get('history', [])
        path = request.path_info

        # Append only if new to avoid duplicate consecutive entries
        if not history or history[-1] != path:
            history.append(path)
            # Trim to the most recent `max_len` entries
            if len(history) > self.max_len:
                history = history[-self.max_len:]
            request.session['history'] = history
            request.session.modified = True
        return None
