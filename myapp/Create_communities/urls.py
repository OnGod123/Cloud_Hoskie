from django.urls import path
from .views import (
    CommunityView, CommentView, RetweetView,
    TweetView, VideoLikeView, TweetLikeView
)

urlpatterns = [
    # Community
    path('communities/', CommunityView.as_view()),
    path('communities/<int:community_id>/', CommunityView.as_view()),
    path('communities/<int:community_id>/members/<int:person_id>/', CommunityView.as_view(), name='add_member'),

    # Comments
    path('communities/<int:community_id>/tweets/<int:tweet_id>/comments/', CommentView.as_view(), name='add_comment'),

    # Retweets
    path('communities/<int:community_id>/retweets/', RetweetView.as_view(), name='retweets'),

    # Tweets
    path('communities/<int:community_id>/tweets/', TweetView.as_view(), name='tweets'),

    # Likes
    path('communities/<int:community_id>/videos/<int:video_id>/like/', VideoLikeView.as_view(), name='video_like'),
    path('communities/<int:community_id>/tweets/<int:tweet_id>/like/', TweetLikeView.as_view(), name='tweet_like'),
]

