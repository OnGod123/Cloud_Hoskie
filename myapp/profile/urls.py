# myapp/profile/urls.py
from django.urls import path
from .views import all_user_profiles, user_profile_by_username  # Import views

urlpatterns = [
    path('', all_user_profiles, name='user_profile'),  # Matches /profile/ to list all profiles
    path('<str:username>/', user_profile_by_username, name='user_profile_by_username'),  # Matches /profile/username/
]