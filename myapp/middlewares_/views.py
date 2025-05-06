from django.http import JsonResponse
from django.views import View

class PreviousURLView(View):
    """
    Returns JSON {previous_url: str or null}
    """
    def get(self, request, *args, **kwargs):
        history = request.session.get('history', [])
        prev = history[-2] if len(history) >= 2 else None
        return JsonResponse({'previous_url': prev})
