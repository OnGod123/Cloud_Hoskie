from django.urls import path, include
from myapp.authentication.views import login_view
from allauth.socialaccount.views import SignupView  # Using SignupView as an example
from myapp.views import home, create_account
from django.views.generic import RedirectView

urlpatterns = [
    path('create_account/', create_account, name='submit'),
    path('', RedirectView.as_view(url='/home', permanent=False)),
    path('home', home, name='home'),
    path('login/facebook/', include('allauth.socialaccount.urls')),  # Using allauth URLs directly
    path('login/gmail/', include('allauth.socialaccount.urls')),
    path('login/instagram/', include('allauth.socialaccount.urls')),
]
