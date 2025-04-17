# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload_video/<int:community_id>/', views.upload_video, name='upload_video'),
    path('community_videos/<int:community_id>/', views.community_videos, name='community_videos'),
]
