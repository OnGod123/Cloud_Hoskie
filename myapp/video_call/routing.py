# myapp/video_call/routing.py
from django.urls import re_path
from . import consumers
from .consumers import SimpleWebSocketConsumer

websocket_urlpatterns = [
   re_path(r'ws/simple/$', consumers.SimpleWebSocketConsumer.as_asgi()),
   re_path(r'^ws/webrtc/(?P<initiator>\w+)/(?P<recipient>\w+)/$', consumers.WebRTCConsumer.as_asgi())
]
