import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.video_call.routing import websocket_urlpatterns  # Correct import here

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cloud_Hoskie.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Directly reference the imported variable
        )
    ),
})
