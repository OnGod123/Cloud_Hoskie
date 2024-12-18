from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from myapp.models import Person
import os
@login_required
def chat_view(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    messages = Message.objects.filter(
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient]
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'messages': messages,
        'recipientUsername': recipient.username,
        'username': request.user.username
    })

@csrf_exempt
@login_required
def upload_voice_message(request):
    try:
        if request.method == 'POST' and request.FILES['voice_file']:
            recipient_id = request.POST.get('recipient_id')
            recipient = get_object_or_404(Person, id=recipient_id)

            voice_file = request.FILES['voice_file']

            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                message_type='voice',
                voice_file=voice_file
            )

            return JsonResponse({'status': 'success', 'message': 'Voice message uploaded successfully!'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request method or no file provided'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
```