from myapp.models import Person
class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")  # Reference to the related tweet
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Person who made the comment
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for comment update

    def __str__(self):
        return f"Comment by {self.person.name} on {self.tweet.content[:20]}"

    @property
    def person_image(self):
        """Fetch the image of the person who made the comment."""
        return self.person.image.url if self.person.image else None