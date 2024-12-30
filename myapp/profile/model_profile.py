from django.db import models
import uuid
from myapp.models import Person

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    user_video = models.URLField(blank=True)
    social_media_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.username = self.person.username
        self.social_media_url = self.person.social_media_api.get('primary_api', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person.name}'s Profile"
  
    def save(self, *args, **kwargs):
        # Generate face encoding if a profile picture is provided
        if self.profile_picture:
            image_path = self.profile_picture.path
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                self.face_encoding = encodings[0].tolist()  # Store encoding as a JSON-serializable list
            else:
                self.face_encoding = None  # No face detected in the profile picture

        self.username = self.person.username
        self.social_media_url = self.person.social_media_api.get("primary_api", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person.name}'s Profile"