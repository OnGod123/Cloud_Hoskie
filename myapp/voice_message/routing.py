from myapp.voice_message.consumers import ChatConsumer  # Correct import of ChatConsumer class
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/voice_messaging/(?P<username>[^/]+)/(?P<recipientUsername>[^/]+)/$', ChatConsumer.as_asgi()),
]
