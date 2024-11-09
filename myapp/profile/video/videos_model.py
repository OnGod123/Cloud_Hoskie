from django.db import models 
from myapp.models import Person 
class Video(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  
    video_file = models.FileField(upload_to='videos/')  
    title = models.CharField(max_length=200)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.person.name}"
