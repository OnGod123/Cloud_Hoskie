from django.db import models
from django.utils import timezone
from myapp.models import Person 

class ChatSession(models.Model):
    """
    Represents an active or historical chat session between two users.
    """
    initiator = models.ForeignKey(Person, related_name="sessions_for_chat", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Person, related_name="received_chats", on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat between {self.initiator.username} and {self.recipient.username} - {'Active' if self.active else 'Ended'}"


class ChatMessage(models.Model):
    """
    Represents a single chat message in a ChatSession.
    """
    session = models.ForeignKey(ChatSession, related_name="message_database", on_delete=models.CASCADE)
    sender = models.ForeignKey(Person, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    delivered = models.BooleanField(default=False)  # Whether the recipient received the message

    def __str__(self):
        return f"Message from {self.sender.username} in session {self.session.id}"


class TypingIndicator(models.Model):
    """
    Tracks whether a user is typing in a specific session.
    """
    session = models.ForeignKey(ChatSession, related_name="indicators_for_typing", on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} typing: {self.is_typing}"
