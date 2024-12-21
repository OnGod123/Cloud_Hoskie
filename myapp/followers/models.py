# models.py
from django.db import models
from myapp.models import Person  # Assuming your Person model is in 'myapp'

class Follow(models.Model):
    follower = models.ForeignKey(Person, related_name="following", on_delete=models.CASCADE)  # Person who is following
    followed = models.ForeignKey(Person, related_name="followers", on_delete=models.CASCADE)  # Person who is being followed
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the follow occurred

    class Meta:
        unique_together = ('follower', 'followed')  # Ensure a person can only follow another person once

    def __str__(self):
        return f"{self.follower.name} follows {self.followed.name}"
