from django.urls import re_path
from .consumers import FileUploadConsumer

websocket_urlpatterns = [
    re_path(r'ws/file_upload/$', FileUploadConsumer.as_asgi()),
]
