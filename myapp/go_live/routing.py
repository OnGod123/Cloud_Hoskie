from django.urls import re_path
from .consumers import LiveSessionConsumer  

# Define WebSocket routes
websocket_urlpatterns = [
    re_path(r"^ws/live_session/(?P<session_id>\d+)/$", LiveSessionConsumer.as_asgi()),
]
