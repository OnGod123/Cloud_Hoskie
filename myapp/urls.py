from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example path
    path('submit/', views.submit, name='submit'),
    path('accounts/', include('allauth.urls')), 
    path('home/', views.home, name='home'),
    
]

