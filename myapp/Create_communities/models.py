from django.db import models
from django.utils import timezone
import uuid

class Community(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(Person, through='CommunityMember', related_name='communities')

    def add_member(self, person, role='member'):
        if not CommunityMember.objects.filter(community=self, person=person).exists():
            CommunityMember.objects.create(community=self, person=person, role=role)
            self.updated_at = timezone.now()
            self.save()

    def __str__(self):
        return self.name


# CommunityMember Model to associate Person with Community
class CommunityMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person.name} as {self.get_role_display()} in {self.community.name}"


# Profile Model
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='profiles')
    username = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.username = self.person.name  # Set username based on Person model
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.person.name}"


# Video Model
class Video(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.person.name} in {self.community.name}"


# Tweet Model
class Tweet(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    mentions = models.TextField(blank=True, null=True)
    trends = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person.name}'s Tweet: {self.content[:20]}"


# Retweet Model
class Retweet(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    original_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='retweets')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Retweet by {self.person.name} on {self.original_tweet.content[:20]}'


# Comment Model
class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.person.name} on {self.tweet.content[:20]}"


# Like Model
class Like(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('person', 'tweet', 'community')

    def __str__(self):
        return f"{self.person.name} liked {self.tweet}"


# ChatSession Model
class ChatSession(models.Model):
    initiator = models.ForeignKey(Person, related_name="initiated_chats", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Person, related_name="received_chats", on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat between {self.initiator.name} and {self.recipient.name} - {'Active' if self.active else 'Ended'}"


# ChatMessage Model
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(Person, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.name} in session {self.session.id}"


# TypingIndicator Model
class TypingIndicator(models.Model):
    session = models.ForeignKey(ChatSession, related_name="typing_indicators", on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} typing: {self.is_typing}"


# Message Model for voice/text messages
class Voice_essage(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_voice_messages')
    recipient = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='received_voice_messages')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('voice', 'Voice')], default='text')
    voice_file = models.FileField(upload_to='voice_messages/', blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender.name} to {self.recipient.name} ({self.timestamp})"


# LiveSession Model
class LiveSession(models.Model):
    host = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hosted_sessions')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.host.name}"
