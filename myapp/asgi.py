import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import WebSocket URL patterns from different apps
from myapp.chat.routings import websocket_urlpatterns as chat_patterns
from myapp.voice_message.route import websocket_urlpatterns as voice_message_patterns
from myapp.go_live.routing import websocket_urlpatterns as go_live_patterns
from myapp.file_upload.routing import websocket_urlpatterns as upload_file_patterns
from myapp.video_call.routing import websocket_urlpatterns as video_call_patterns
from myapp.profile.video.video_streaming.routing import websocket_urlpatterns as video_streaming_patterns

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

# Create the Django ASGI application
django_asgi_app = get_asgi_application()

# Combine WebSocket URL patterns from all apps
websocket_urlpatterns = chat_patterns + voice_message_patterns + go_live_patterns + upload_file_patterns + video_call_patterns + video_streaming_patterns


# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Handle HTTP traffic
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Combined WebSocket traffic
        )
    ),
})
