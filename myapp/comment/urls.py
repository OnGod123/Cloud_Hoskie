from django.urls import path
from .views import comment_view

urlpatterns = [
    path("comments/", comment_view, name="comment_view"),
]
