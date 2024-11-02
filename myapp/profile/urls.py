# myprofile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hoskie/profile/<uuid:profile_id>/', views.serve_profile_view, name='serve_profile'),
    path('hoskie/profile/<str:username>/', views.user_profile_by_username, name='user_profile_by_username'),
]
