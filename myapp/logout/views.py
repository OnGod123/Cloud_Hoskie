# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpRequest
from .models import LogoutActivity
from django.contrib.auth.decorators import login_required

@login_required
def custom_logout(request: HttpRequest):
    if request.user.is_authenticated:
        # Log the user logout event
        LogoutActivity.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            ip_address=request.META.get('REMOTE_ADDR')  # Logs the user's IP address
        )

        # Clear session data
        logout(request)
        request.session.flush()  # Clears all session data

        # Invalidate any authentication tokens (e.g., for API access)
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        # Add a feedback message
        messages.info(request, "You have successfully logged out.")
    
    return redirect('login')  # Redirect to login or other specified page
