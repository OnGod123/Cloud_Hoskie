from django.urls import path, include
from . import views
from myapp.authentication.views import login_view  # Import your login_view

urlpatterns = [
    path('', views.index, name='index'),  # Example path
    path('submit/', views.submit, name='submit'),
    path('accounts/', include('allauth.urls')), 
    path('home/', views.home, name='home'),
    path('login/', login_view, name='login'),  # Add this line for the login view
]
