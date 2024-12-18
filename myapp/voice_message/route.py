websocket_urlpatterns = [
    re_path(r'ws/messaging/(?P<username>[^/]+)/(?P<recipientUsername>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
```
