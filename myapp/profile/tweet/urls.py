# myapp/profile/tweet/urls.py

from django.urls import path
from .views import tweet_view, retweet_view  # Import both tweet_view and retweet_view

urlpatterns = [
    path('retweet/', retweet_view, name='retweet'),  # Corrected the import reference here
    path('tweet/', tweet_view, name='tweet_view'),  # Fixed the space issue, use 'tweet/' path
]
