from django.db import models
from myapp.models import Person

class File(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10, choices=[
        ('text', 'Text'),
        ('file', 'File'),
    ], default='text')
    uploaded_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)  # Accepts any file type

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} ({self.timestamp})"