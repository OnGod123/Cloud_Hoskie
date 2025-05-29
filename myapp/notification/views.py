# myapp/notifications/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from myapp.notifications.models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/list.html', {'notifications': notifications})

