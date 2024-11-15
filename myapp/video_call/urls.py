from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns
    path('<str:recipient>/', views.voice_call_view, name='videocall'),
]
