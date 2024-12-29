from django.db import models
from myapp.models import Person
from myapp.profile.tweet.tweet_models import Tweet


class Like(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Reference to Person who liked the tweet
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)  # The tweet that is liked
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the like occurred

    class Meta:
        unique_together = ('person', 'tweet')  # Ensure a person can only like a tweet once
