# myapp/routing.py

from django.urls import path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    path('ws/videos/', VideoStreamConsumer.as_asgi()),  # WebSocket route for video streaming
]
