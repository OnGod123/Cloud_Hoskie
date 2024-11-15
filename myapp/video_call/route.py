# myapp/video_call/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/webrtc/<str:initiator>/<str:recipient>/', consumers.WebRTCConsumer.as_asgi()),
]
