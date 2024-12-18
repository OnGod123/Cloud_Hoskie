import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from file_app.routing import websocket_urlpatterns  # Adjust `file_app` to your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_hoske.settings')  # Replace `myproject` with your project name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
