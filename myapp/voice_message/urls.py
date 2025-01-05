from django.urls import path  # Import the path function
from .views import voice_message  # Import your view

urlpatterns = [
    path('/<str:recipient_username>/', voice_message, name='start_chat_session'),
    
 ]
