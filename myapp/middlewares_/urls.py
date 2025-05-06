from django.urls import path
from .views import previous_url_ajax

urlpatterns = [
    # … your other profile URLs …
    path('ajax/previous-url/', previous_url_ajax, name='previous-url-ajax'),
]

