📑 User Session Management (Login/Logout) - Cloud_Hoskie
This document explains how user sessions (login, logout, authentication flow) are handled in the Cloud_Hoskie project.

🛠 Overview
We have implemented a custom session handling system with:

Secure Login at /sign-in/

Proper Logout at /logout/

Clear session invalidation on logout

Custom redirects after login/logout

Session cookies (sessionid, csrftoken) removed on logout

Logout activity tracking (user, time, IP)

📌 How it Works

Action	URL	Function	Behavior
Login	/sign-in/	login_view	Authenticates user and starts session
Logout	/logout/	custom_logout	Ends session, clears cookies, logs logout event
🔥 Session Details
Login:

User logs in via /sign-in/.

After successful login:

Redirects to /home/ (LOGIN_REDIRECT_URL).

Session cookie (sessionid) is set automatically.

Logout:

User logs out via /logout/.

Process:

logout(request) — kills the Django session.

request.session.flush() — clears all session data.

Deletes cookies sessionid and csrftoken.

Logs the logout event (LogoutActivity model).

Redirects user to / (ACCOUNT_LOGOUT_REDIRECT_URL).

⚙️ Settings
In settings.py:

python
Copy
Edit
LOGIN_URL = '/sign-in/'        # Where @login_required redirects unauthenticated users
LOGIN_REDIRECT_URL = '/home/'  # After login, go to home
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # After logout, go to landing page
📂 URL Setup
In Cloud_Hoskie/urls.py:

python
Copy
Edit
urlpatterns = [
    path('sign-in/', include('myapp.authentication.urls')),
    path('logout/', include('myapp.logout.urls')),
    ...
]
In myapp/authentication/urls.py:

python
Copy
Edit
urlpatterns = [
    path('', views.login_view, name='sign_in'),
]
In myapp/logout/urls.py:

python
Copy
Edit
urlpatterns = [
    path('', views.custom_logout, name='logout'),
]
📋 Notes
Why delete cookies manually?

For extra security, especially when using API tokens or sensitive session data.

LogoutActivity model records:

User ID

Logout timestamp

IP Address

Custom redirection avoids broken links like /accounts/login/ errors.

🚀 Future Improvements
Add Remember Me functionality (longer session expiry).

Integrate multi-device logout (invalidate all sessions).

Add logout from API endpoints for mobile apps.

✅ Status: Working and Stable
User login/logout/session management is now fully functional, secure, and ready for production! 🚀

Would you also like a LogoutActivity model README or schema description separately? 📜
It would be helpful for your backend documentation later! 🌟








