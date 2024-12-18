from django.urls import path
from . import views

urlpatterns = [
    path('live_session/create/', views.create_live_session, name='create_live_session'),
    path('live_session/<int:session_id>/', views.join_live_session, name='join_live_session'),
]
