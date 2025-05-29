import uuid
from django.db import models
from django.utils import timezone
from myapp.models import Person
from .models import ConnectionLogic  # ensure correct import if in different app

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        Person,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        Person,
        related_name='actor_notifications',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)   # e.g. "sent you a connection request"
    target = models.UUIDField(null=True, blank=True)  # can store ConnectionLogic.id
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification(to={self.recipient}, verb={self.verb})"
