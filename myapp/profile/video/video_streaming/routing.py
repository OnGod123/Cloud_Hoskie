# myapp/routing.py

from django.urls import re_path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    re_path(r'^ws/video-stream/$', VideoStreamConsumer.as_asgi()),  
]
