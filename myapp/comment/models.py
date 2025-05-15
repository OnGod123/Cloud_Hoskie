from django.db import models
from myapp.profile.tweet.tweet_models import Tweet

class _Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")  # Reference to Tweet
    person = models.ForeignKey('Person', on_delete=models.CASCADE)  # Reference to Person (who made the comment)
    content = models.TextField()  # Comment content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the comment was created

    def __str__(self):
        return f"Comment by {self.person.name}: {self.content[:20]}"

    @property
    def person_uservideo(self):
        """Fetch the `uservideo` from the linked Person."""
        return self.person.uservideo
