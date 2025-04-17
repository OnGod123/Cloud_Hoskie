from django.urls import path
from .consumers import CommunityVoiceChatConsumer

websocket_urlpatterns = [
    path('ws/community/<int:community_id>/', CommunityVoiceChatConsumer.as_asgi()),
]

from django.urls import path
from .consumers import LiveSessionConsumer

websocket_urlpatterns = [
    path('ws/live_session/<int:community_id>/', LiveSessionConsumer.as_asgi()),
]