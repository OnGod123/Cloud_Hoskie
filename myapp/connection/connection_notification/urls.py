from django.urls import path
from .views import notifications_view, mark_read

urlpatterns += [
    path('notifications/', notifications_view, name='notifications'),
    path('notifications/mark-read/<uuid:notification_id>/', mark_read, name='mark_notification_read'),
]
