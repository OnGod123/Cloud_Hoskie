from django.urls import path
from . import views

urlpatterns = [
    path('upload_file_message/', views.upload_file_message, name='upload_file_message'),
]
