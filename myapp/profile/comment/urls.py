from django.urls import path
from .views import comment_view

urlpatterns = [
    path("comments/<tweet_id>", comment_view, name="comment_view"),
]
