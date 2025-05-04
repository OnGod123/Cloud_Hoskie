from django.urls import path
from .search_views import search_view, send_connection_request



urlpatterns = [
    
    path('search/', search_view, name='search'),
    path('connections/send/<uuid:to_user_id>/', send_connection_request, name='send_connection_request'),
]

