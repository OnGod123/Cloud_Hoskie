from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from .models import LogoutActivity
from django.contrib.auth.decorators import login_required

@login_required
def custom_logout(request: HttpRequest):
    if request.user.is_authenticated:
        # Log the user logout event
        LogoutActivity.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            ip_address=request.META.get('REMOTE_ADDR')
        )

        # Invalidate any authentication tokens
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        # Clear session data
        logout(request)
        request.session.flush()

        # Prepare response and delete cookies
        response = HttpResponseRedirect('settings.ACCOUNT_LOGOUT_REDIRECT_URL')  # Or use reverse('login')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')

        # Add a feedback message
        messages.info(request, "You have successfully logged out.")

        return response  # <<< return the prepared response

    return redirect('settings.ACCOUNT_LOGOUT_REDIRECT_URL')  # In case someone weird hits this route without being authenticated

