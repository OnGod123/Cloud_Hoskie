from django.urls import path, include
from myapp.authentication.views import login_view  # Import your login_view
from myapp.video_call.views import voice_call_view  # Import the voice_call_view from video_call.views
from myapp.views import index, submit, home  # Import the general views from myapp/views.py

urlpatterns = [
    path('', index, name='index'),  # Reference the index view from myapp/views.py
    path('submit/', submit, name='submit'),
    path('accounts/', include('allauth.urls')), 
    path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    path('video_call/<str:recipient>/', voice_call_view, name='videocall')  # Reference the voice_call_view from video_call.views
]
