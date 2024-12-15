from django.urls import path
from .views import tweet_view

urlpatterns = [
    path(' ', tweet_view, name='tweet_view'),
]
