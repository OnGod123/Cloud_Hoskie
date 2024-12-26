from django.db import models
from myapp.models import person
class Tweet(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Reference to Person
    content = models.TextField()  # Content of the tweet
    mentions = models.TextField(blank=True, null=True)  # Store mentions (@username)
    trends = models.TextField(blank=True, null=True)  # Store trends (#hashtag)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the tweet was created
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person.name}'s Tweet: {self.content[:20]}"

    @property
    def person_uservideo(self):
        """Fetch the `uservideo` from the linked Person."""
        return self.person.uservideo

class Retweet(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Reference to Person, not User
    original_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='retweets')  # Original tweet being retweeted
    content = models.TextField(blank=True)  # Optionally, users can add their own comment
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Retweet by {self.person.name} on {self.original_tweet.content}'
     @property
    def person_uservideo(self):
        """Fetch the `uservideo` from the linked Person."""
        return self.person.uservideo
