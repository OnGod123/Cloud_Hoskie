from django.urls import path
from myapp._views.dashboard import DashboardView
from myapp._views.views  import PreviousURLView

app_name = 'sessions'

urlpatterns = [
    # Dashboard page
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # AJAX endpoint for getting previous URL
    path('ajax/previous-url/', PreviousURLView.as_view(), name='previous-url-ajax'),
]
