from django.db import models
from myapp.models import Person
class Image(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  
    image_file = models.ImageField(upload_to='images/')  
    caption = models.CharField(max_length=200, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Image by {self.person.name}: {self.caption[:20]}"