from django.urls import path, include
from myapp.authentication.views import login_view  
from allauth.socialaccount.views import OAuthLoginView
from myapp.views import home, create_account  

urlpatterns = [
    path('create_account/', create_account, name='submit'),
    path('', RedirectView.as_view(url='/home', permanent=False)), 
    path('/home', home, name='home'),
    path('login/facebook/', OAuthLoginView.as_view(), name='facebook_login'),
    path('login/gmail/', OAuthLoginView.as_view(), name='google_login'),
    path('login/instagram/', OAuthLoginView.as_view(), name='instagram_login'),
]
