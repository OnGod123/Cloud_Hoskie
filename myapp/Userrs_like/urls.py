# urls.py
from django.urls import path
from .views import like_view

urlpatterns = [
    path("tweets/<int:tweet_id>/like/", like_view, name="like_view"),
]
