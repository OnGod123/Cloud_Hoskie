from django.urls import path
from .views import tweet_view

urlpatterns = [
    path('tweet/', tweet_view, name='tweet_view'),
]
