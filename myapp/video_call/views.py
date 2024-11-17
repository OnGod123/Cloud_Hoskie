from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required

# @login_required

def voice_call_view(request, recipient):
    # Assuming the recipient is the target username passed in the URL
    recipient_user = get_object_or_404(User, username=recipient)

    # Get the authenticated user's username
    #authenticated_user = request.user.username
    authenticated_user = 'vincent'
    print(f"Authenticated user: {authenticated_user}")
    print(f"Recipient username: {recipient_user.username}")

    # Pass both the authenticated user's username and recipient's username to the template
    return render(request, 'video_call.html', {
        'username': authenticated_user,  # Pass authenticated user's username
        'recipientUsername': recipient_user.username  # Pass recipient's username
    })
