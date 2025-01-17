from django.urls import path
from .views import video_stream_view, share_video  # Import the correct views

urlpatterns = [
    path('video-streaming/', video_stream_view, name='video_streaming'),
    path('share-video/<int:video_id>/', share_video, name='share_video'),
]
