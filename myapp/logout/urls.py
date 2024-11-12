# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_logout, name='logout'),  # The empty path means it will match /logout/
]
