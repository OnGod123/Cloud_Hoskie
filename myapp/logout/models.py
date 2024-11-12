from myapp.models import Person
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LogoutActivity(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} logged out at {self.timestamp}"
