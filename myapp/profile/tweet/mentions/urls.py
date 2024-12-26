from django.urls import path
from .views import MentionView

urlpatterns = [
    path('mentions/', MentionView.as_view(), name='get_mentions'),
    path('mentions/<str:mention>/', MentionView.as_view(), name='get_mention_tweets'),
]
