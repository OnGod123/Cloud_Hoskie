from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import _Comment, Tweet
from myapp.models import Person

@csrf_exempt
def comment_view(request, tweet_id):
    if request.method == "GET":
        # Fetch all comments for the specific tweet
        comments = _Comment.objects.filter(tweet__id=tweet_id).select_related('person')
        comment_data = [
            {
                'comment_id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'person_name': comment.person.name,
                'person_image': comment.person.image.url  # Adjusted for FileField
            }
            for comment in comments
        ]

        # Send back initial data
        tweet = Tweet.objects.get(id=tweet_id)
        comment_input = {
            'comment': "",
            'placeholder': "Add your comment here...",
            'tweet_id': tweet.id,
            'person_name': request.user.person.name,  # Assuming authenticated user
            'person_image': request.user.person.image.url
        }
        return JsonResponse({"comments": comment_data, "comment_input": comment_input})

    elif request.method == "POST":
        # Handle comment creation
        data = json.loads(request.body)
        content = data.get("content")
        if not content:
            return JsonResponse({"error": "Content is required"}, status=400)

        try:
            person = request.user.person
            tweet = Tweet.objects.get(id=tweet_id)
            comment = _Comment.objects.create(
                tweet=tweet,
                person=person,
                content=content
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({
            "message": "Comment created successfully",
            "comment_id": comment.id
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)
