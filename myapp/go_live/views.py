from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import LiveSession

@login_required
def create_live_session(request):
    """Create a new live session."""
    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        session = LiveSession.objects.create(host=request.user, title=title, is_active=True)
        return JsonResponse({"message": "Live session created", "session_id": session.id})

    return render(request, "create_live_session.html")


@login_required
def join_live_session(request, session_id):
    """Join an existing live session."""
    session = get_object_or_404(LiveSession, id=session_id, is_active=True)
    return render(request, "live_session.html", {"session": session})
