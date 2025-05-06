
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SessionHistoryMiddleware(MiddlewareMixin):
    """
    Tracks the last SESSION_HISTORY_MAX_LENGTH visited paths in session['history'].
    Skips duplicate consecutive entries and any AJAX-only fetches.
    """
    def process_request(self, request):
        # Only track GET navigations for HTML (not AJAX fragments, media, etc.)
        if request.method != 'GET' or request.is_ajax():
            return

        max_len = getattr(settings, 'SESSION_HISTORY_MAX_LENGTH', 10)
        history = request.session.get('history', [])

        current = request.path_info
        if not history or history[-1] != current:
            history.append(current)
            # Trim to last N
            if len(history) > max_len:
                history = history[-max_len:]

            request.session['history'] = history
            request.session.modified = True
