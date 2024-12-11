from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_page, name='video_render'),       
    path('upload/', views.upload_video, name='video_upload'), 
    path('capture/', views.capture_video, name='video_capture'),
]
