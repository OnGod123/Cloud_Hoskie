from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('capture/', views.capture_image, name='capture_image'),
    path('page/', views.render_image_page, name='render_image_page'),
]
