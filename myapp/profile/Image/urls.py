from django.urls import path
from . import views

urlpatterns = [
    path('image/upload/', views.upload_image, name='upload_image'),
    path('image/capture/', views.capture_image, name='capture_image'),
    path('image/page/', views.render_image_page, name='render_image_page'),
]
