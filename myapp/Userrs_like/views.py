# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Like, Tweet
from myapp.models import Person
import json

@csrf_exempt
def like_view(request, tweet_id):
    if request.method == "POST":
        # Handle like/unlike
        try:
            tweet = Tweet.objects.get(id=tweet_id)
            person = request.user.person  # Assuming the user is authenticated and has a 'person' attribute

            # Check if the person has already liked this tweet
            existing_like = Like.objects.filter(person=person, tweet=tweet).first()

            if existing_like:
                # Unlike: delete the like
                existing_like.delete()
                return JsonResponse({"message": "Tweet unliked successfully", "liked": False})

            else:
                # Like: create a new like
                Like.objects.create(person=person, tweet=tweet)
                return JsonResponse({"message": "Tweet liked successfully", "liked": True})

        except Tweet.DoesNotExist:
            return JsonResponse({"error": "Tweet not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
