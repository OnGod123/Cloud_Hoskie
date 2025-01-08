from django.urls import path
from .views import render_page  # Import the render_page view

urlpatterns = [
    path('video-streaming/', render_page, name='video_streaming'), 
]
