from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include('myapp.urls')),
    path('profile/', include('myapp.profile.urls')),
    path('search/', include('myapp.elastic_search.urls')),
    path('logout/', include('myapp.logout.urls')),
    path('video-call/', include('myapp.video_call.urls')),
    path('video/', include('myapp.profile.video.urls')),
    path('chat/', include('myapp.chat.urls')),
    path('Tweet/', include('myapp.Tweet.urls')),  # Fixed missing parenthesis
    path('Voice_messaging/', include('myapp.Voice_message.urls')),  # Fixed capitalization and missing parenthesis
    path('live_app/', include('myapp.live_go.urls')),
    path(" ", include('myapp.file_upload.urls')),  # Fixed capitalization of 'imclude'
    path(" ", include('myapp.wallet.urls')),
    path(" ", include('myapp.authenticate.urls')),  # Fixed missing parenthesis
    path('image/', include('myapp.profile.Image.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)

