from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from django.shortcuts import render

def file_upload_page(request):
    return render(request, "file_upload.html")

@csrf_exempt
@login_required
def upload_file_message(request):
    try:
        if request.method == 'POST' and request.FILES['uploaded_file']:
            recipient_id = request.POST.get('recipient_id')
            recipient = get_object_or_404(User, id=recipient_id)

            uploaded_file = request.FILES['uploaded_file']
            
            # Optional: Validate file size (e.g., max 10 MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                raise ValidationError("File size exceeds 10 MB limit")

            # Save file message to database
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                message_type='file',
                uploaded_file=uploaded_file
            )

            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid request or file not provided'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
