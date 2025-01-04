from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ChatSession, ChatMessage, TypingIndicator
from myapp.models import Person  # Assuming 'Person' model is part of your app

@login_required
def chat_view(request, recipient):
    """
    Render the chat interface between the authenticated user and the recipient.
    Handle GET and POST methods:
    - GET: Render the chat frontend.
    - POST: Save a new message to the chat session.
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

        if request.method == 'GET':
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

        elif request.method == 'POST':
            # Save a new message to the chat session
            message_text = request.POST.get('message', '').strip()
            if not message_text:
                return HttpResponseBadRequest("Message content cannot be empty.")

            new_message = ChatMessage.objects.create(
                session=chat_session,
                sender=initiator,
                content=message_text
            )

            return JsonResponse({
                'message': "Message sent successfully.",
                'chat_session_id': chat_session.id,
                'message_id': new_message.id,
                'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'sender': new_message.sender.username
            })

    except ValidationError as e:
        # Handle any validation errors and provide user-friendly feedback
        return HttpResponseBadRequest(f"Invalid request: {e}")
    except Exception as e:
        # Generic fallback for unexpected errors (log it in real applications)
        return render(request, 'error.html', {
            'error_message': "An unexpected error occurred. Please try again later."
        })


def all_chat_sessions(request):
    return JsonResponse({"message": "All chat sessions endpoint"})

def chat_session_detail(request, session_id):
    return JsonResponse({"message": f"Chat session detail for session {session_id}"})

def start_chat_session(request, recipient_username):
    return JsonResponse({"message": f"Starting chat session with {recipient_username}"})

def send_message(request, session_id):
    return JsonResponse({"message": f"Message sent in session {session_id}"})

def typing_status(request, session_id):
    return JsonResponse({"message": f"Typing status for session {session_id}"})