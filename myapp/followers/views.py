# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Person
from .models import Follow
import json

@csrf_exempt
def follow_view(request, person_id):
    if request.method == "POST":
        try:
            person_to_follow = Person.objects.get(id=person_id)
            follower = request.user.person  # Assuming the user is authenticated and has a 'person' attribute

            # Check if the person is trying to follow themselves
            if person_to_follow == follower:
                return JsonResponse({"error": "You cannot follow yourself"}, status=400)

            # Check if the person is already following the other person
            existing_follow = Follow.objects.filter(follower=follower, followed=person_to_follow).first()

            if existing_follow:
                # Unfollow: delete the follow relationship
                existing_follow.delete()
                return JsonResponse({"message": "Unfollowed successfully", "following": False})

            else:
                # Follow: create a new follow relationship
                Follow.objects.create(follower=follower, followed=person_to_follow)
                return JsonResponse({"message": "Followed successfully", "following": True})

        except Person.DoesNotExist:
            return JsonResponse({"error": "Person not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
