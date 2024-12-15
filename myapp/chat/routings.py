from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<initiator>\w+)/(?P<recipient>\w+)/$', consumers.ChatConsumer.as_asgi()),
]