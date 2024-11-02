from django.db import models 
from myapp.models import Person  
class Tweet(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Reference to Person
    content = models.TextField()  # Content of the tweet
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the tweet was created

    def __str__(self):
        return f"{self.person.name}'s Tweet: {self.content[:20]}"
