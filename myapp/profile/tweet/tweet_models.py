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
