from django.db import models
from myapp.models import Person

class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_messages')
    recipient =
 models.ForeignKey(Person, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10, choices=[
        ('text', 'Text'),
        ('voice', 'Voice')
    ], default='text')
    voice_file = models.FileField(upload_to='voice_messages/', blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} ({self.timestamp})"
```
