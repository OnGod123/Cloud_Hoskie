from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('profile/', include('myapp.profile.urls')),
    path('search/', include('myapp.elastic_search.urls')),
    path('logout/', include('myapp.logout.urls')),
    path('video-call/', include('myapp.video_call.urls')),
    path('video/', include('myapp.profile.video.urls')),
    path('chat/', include('myapp.chat.urls')),
    path('tweet/', include('myapp.profile.tweet.urls')),  # Lowercase "tweet" for consistency
    path('voice-messaging/', include('myapp.voice_message.urls')),
    path('live-app/', include('myapp.go_live.urls')),
    path('file-upload/', include('myapp.file_upload.urls')),
    path('wallet/', include('myapp.wallet.urls')),
    path('sign-in/', include('myapp.authentication.urls')),  # <-- Correct spelling and trailing slash!
    path('mentions/', include('myapp.profile.tweet.mentions.urls')),
    path('trends/', include('myapp.profile.tweet.trend_views.urls')),
    path('comments/', include('myapp.comment.urls')),
    path('video-streaming/', include('myapp.profile.video.video_streaming.urls')),
    path('image/', include('myapp.profile.Image.urls')),
    path('create/', include('myapp.Create_communities.urls')),
    path("create_friends", include('myapp.followers.urls')),
    path('', include('myapp.connection.urls')),
    path('', include('myapp.session_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)

