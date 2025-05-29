from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.models import Person
from .models import Notification

@login_required
def notifications_view(request):
    person = Person.objects.get(user=request.user)
    notifications = person.notifications.filter(is_read=False).order_by('-created_at')
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def mark_read(request, notification_id):
    n = Notification.objects.filter(id=notification_id, recipient__user=request.user).first()
    if n:
        n.is_read = True
        n.save()
    return redirect('notifications')
