from django.db import models

from django.contrib.auth.hashers import make_password, check_password
import uuid

class Person(models.Model):
    RELATIONSHIP_CHOICES = (
        ('single', 'Single'),
        ('in_relationship', 'In a Relationship'),
        ('engaged', 'Engaged'),
        ('married', 'Married'),
        ('complicated', 'It\'s Complicated'),
    )

    SEXUAL_ORIENTATION_CHOICES = (
        ('gay', 'Gay'),
        ('lesbian', 'Lesbian'),
        ('straight', 'Straight'),
        ('other', 'Other'),
    )

    RACE_CHOICES = (
        ('white', 'White'),
        ('black', 'Black'),
        ('asian', 'Asian'),
        ('hispanic', 'Hispanic'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, default='default_username')
    name = models.CharField(max_length=60)
    relationship_status = models.CharField(max_length=15, choices=RELATIONSHIP_CHOICES)
    sexual_orientation = models.CharField(max_length=10, choices=SEXUAL_ORIENTATION_CHOICES)
    race = models.CharField(max_length=10, choices=RACE_CHOICES)
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    social_media_api = models.URLField()  # Assuming this will hold social media API URL
    birth_date = models.DateField()
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Password field

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk or Person.objects.filter(pk=self.pk).exists():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        # Check if the provided password matches the stored hashed password
        return check_password(raw_password, self.password)




from django.conf import settings
from django.db import models
from myapp.middleware import get_current_user

class TimeStampedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,          # in case you ever create outside a request
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # only stamp on initial create
        if not self.pk:
            user = get_current_user()
            if user and user.is_authenticated:
                self.created_by = user
        super().save(*args, **kwargs)

