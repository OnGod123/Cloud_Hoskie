"""
URL configuration for Cloud_Hoskie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('profile/', include('myapp.profile.urls')),
    path('search/', include('myapp.elastic_search.urls')),
    path('logout/', include('myapp.logout.urls')),
    path('video-call/', include('myapp.video_call.urls')),
    path('video/', include('myapp.profile.video.urls')),
    path('chat/', include('myapp.chat.urls'),
    path('Tweet/', include('myapp.Tweet.urls'),
    path('Voice_messaging/', Include('myapp.Voice_message.urls'),
    path('live_app/', include('myapp.live_go.urls')),
    path(" ", imclude('myapp.file_upload.urls')),
    path(" ", include('myapp.wallet.urls')),
    path('image/', include('myapp.profile.Image.urls'))
]

if settings.DEBUG:
     urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)
     urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)