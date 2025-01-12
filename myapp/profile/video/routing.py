from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video-stream/', consumers.VideoStreamConsumer.as_asgi(), name='video_stream'),
]
