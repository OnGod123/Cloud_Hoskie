from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class PreviousURLView(View):
    """
    Returns the previous non-AJAX URL from session history as JSON.

    GET response: { "previous_url": <string|null> }
    """
    def get(self, request, *args, **kwargs):
        history = request.session.get('history', [])
        previous = history[-2] if len(history) >= 2 else None
        return JsonResponse({'previous_url': previous})
