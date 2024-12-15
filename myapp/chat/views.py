from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ChatSession, ChatMessage, TypingIndicator
from myapp.models import Person  # Assuming 'Person' model is part of your app

@login_required
def chat_view(request, recipient):
    """
    Render the chat interface between the authenticated user and the recipient.
    If a chat session doesn't exist, create a new one.
    """
    try:
        # Ensure the recipient exists in the database
        recipient_user = get_object_or_404(Person, username=recipient)

        # Check if the user is trying to chat with themselves
        if request.user.username == recipient_user.username:
            return HttpResponseBadRequest("You cannot start a chat session with yourself.")

        # Get the currently logged-in user (as a 'Person' model object)
        initiator = get_object_or_404(Person, username=request.user.username)
        recipient_person = get_object_or_404(Person, username=recipient_user.username)

        # Try to find an existing active chat session between the two users
        chat_session = ChatSession.objects.filter(
            initiator=initiator, recipient=recipient_person, active=True
        ).first()

        # If no active session exists, create a new chat session
        if not chat_session:
            chat_session = ChatSession.objects.create(
                initiator=initiator,
                recipient=recipient_person,
                active=True
            )

        # Get chat messages related to the session
        messages = ChatMessage.objects.filter(session=chat_session).order_by('timestamp')

        # Typing indicator (check if the recipient is typing)
        typing_indicator = TypingIndicator.objects.filter(
            session=chat_session, user=recipient_person
        ).first()

        # Pass session, messages, and typing indicator status to the template
        return render(request, 'chat.html', {
            'username': initiator.username,  # The logged-in user's username
            'recipientUsername': recipient_person.username,  # The recipient's username
            'chat_session': chat_session,  # Chat session data
            'messages': messages,  # Messages in the session
            'typing_indicator': typing_indicator.is_typing if typing_indicator else False  # Typing status
        })

    except ValidationError as e:
        # Handle any validation errors and provide user-friendly feedback
        return HttpResponseBadRequest(f"Invalid request: {e}")
    except Exception as e:
        # Generic fallback for unexpected errors (log it in real applications)
        return render(request, 'error.html', {
            'error_message': "An unexpected error occurred. Please try again later."
        })
