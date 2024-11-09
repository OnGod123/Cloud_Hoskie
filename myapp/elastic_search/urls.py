# myapp/urls.py (App-Level URL Configuration)

from django.urls import path
from .views import get_profiles, autocomplete_video, autocomplete_tweet, autocomplete_image

urlpatterns = [
    # Root URL Search (general search for profiles, videos, tweets, etc.)
    path('', get_profiles, name='root_search'),  # This is now under '/search/'

    # Subroot URL Search (search profiles by username)
    path('username/<str:username>/', get_profiles, name='search_by_username'),

    # Autocomplete for other models (videos, tweets, images)
    path('search/video/', autocomplete_video, name='autocomplete_video'),
    path('searchlete/tweet/', autocomplete_tweet, name='autocomplete_tweet'),
    path('search/image/', autocomplete_image, name='autocomplete_image'),
]
