import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.chat.routings import websocket_urlpatterns as chat_routes
from myapp.voice_message.routing import websocket_urlpatterns as voice_routes
from myapp.go_live.routing import websocket_urlpatterns as live_routes
from myapp.file_upload.routing import websocket_urlpatterns as upload_routes
from myapp.profile.video.video_streaming.routing import websocket_urlpatterns as stream_routes  # Correct import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cloud_Hoskie.settings')
websocket_urlpatterns =  chat_routes + voice_routes + live_routes + upload_routes + stream_routes
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

