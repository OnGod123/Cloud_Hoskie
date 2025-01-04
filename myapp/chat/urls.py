from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.all_chat_sessions, name='all_chat_sessions'),
    path('session/<int:session_id>/', views.chat_session_detail, name='chat_session_detail'),
    path('session/start/<str:recipient_username>/', views.start_chat_session, name='start_chat_session'),
    path('session/<int:session_id>/send/', views.send_message, name='send_message'),
    path('session/<int:session_id>/typing/', views.typing_status, name='typing_status'),
    path('/<str:recipient>/', views.chat_view, name='voice_chat_view'),
]
