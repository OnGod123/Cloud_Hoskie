from django.urls import path
from .views import TrendView

urlpatterns = [
    path('', TrendView.as_view(), name='get_trends'),
    path('trends/<str:trend>/', TrendView.as_view(), name='get_trend_tweets'),
]
