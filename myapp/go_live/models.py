from django.db import models
from myapp.mpdels import Person

class LiveSession(models.Model):
    host = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hosted_sessions')
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.host.username}"
