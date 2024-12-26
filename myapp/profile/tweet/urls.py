from django.urls import path
from .views import tweet_view

urlpatterns = [
    path('retweet/', views.retweet_view, name='retweet'),
    path(' ', tweet_view, name='tweet_view'),
]
