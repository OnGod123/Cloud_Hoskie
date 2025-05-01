import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.profile.video.video_streaming.routing import websocket_urlpatterns  # Correct import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cloud_Hoskie.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

