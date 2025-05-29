
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from myapp.notifications.models import Notification
from myapp.profile.tweet.tweet_models import Comment, Like, Retweet
from myapp.models import Follow

def make_notification(instance, verb, recipient):
    Notification.objects.create(
        recipient    = recipient,
        sender       = instance.created_by,  # stamp comes from TimeStampedModel
        verb         = verb,
        content_type = ContentType.objects.get_for_model(instance),
        object_id    = instance.pk
    )

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if not created: return
    recipient = instance.tweet.person.user
    make_notification(instance, "commented on", recipient)

@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    if not created: return
    recipient = instance.tweet.person.user
    make_notification(instance, "liked", recipient)

@receiver(post_save, sender=Retweet)
def retweet_notification(sender, instance, created, **kwargs):
    if not created: return
    recipient = instance.original_tweet.person.user
    make_notification(instance, "retweeted", recipient)

@receiver(post_save, sender=Follow)
def follow_notification(sender, instance, created, **kwargs):
    if not created: return
    recipient = instance.followed.user
    make_notification(instance, "followed you", recipient)

