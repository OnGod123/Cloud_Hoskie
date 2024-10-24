from django.db import models

class UserProfile(models.Model):
    email = models.EmailField(unique=True)  # Email field (compulsory)
    password = models.CharField(max_length=128)  # Password field (compulsory)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)  # Image field (optional)
    person = models.OneToOneField('myapp.Person', on_delete=models.CASCADE)  # Use string notation to avoid import issues
    verified = models.BooleanField(default=False)  # Verified field (not compulsory)
    login_count = models.IntegerField(default=0)  # Track login attempts
    session_active = models.BooleanField(default=False)  # Track if the session is active

    def increment_login_count(self):
        self.login_count += 1
        self.save()

    def start_session(self):
        self.session_active = True
        self.save()

    def end_session(self):
        self.session_active = False
        self.save()

    @property
    def person(self):
        from myapp.models import Person  # Import here to avoid circular import
        return self._person

    @person.setter
    def person(self, value):
        from myapp.models import Person  # Import here to avoid circular import
        self._person = value
