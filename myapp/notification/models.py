from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from myapp.models import TimeStampedModel

class Notification(TimeStampedModel):
    recipient    = models.ForeignKey(
                      settings.AUTH_USER_MODEL,
                      related_name="notifications",
                      on_delete=models.CASCADE
                   )
    sender       = models.ForeignKey(
                      settings.AUTH_USER_MODEL,
                      related_name="sent_notifications",
                      on_delete=models.CASCADE
                   )
    verb         = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    target       = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.sender} {self.verb} you"

