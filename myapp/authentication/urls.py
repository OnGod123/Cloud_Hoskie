from django.urls import path
from . import views  

urlpatterns = [
    # URL for the sign-in view
    path('sign-in/', views.login_view, name='sign_in')
]

