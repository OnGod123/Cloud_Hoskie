from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .tweet_models import Tweet, Retweet
from myapp.models import Person
import json
import re
from django.contrib.auth.decorators import login_required

@csrf_exempt
def tweet_view(request):
    if request.method == "GET":
        # Fetch all tweets along with their related person data
        tweets = Tweet.objects.select_related('person').all()

        # Render tweets in the HTML template
        return render(request, 'tweets.html', {'tweets': tweets})

    elif request.method == "POST":
        try:
            # Parse the JSON body from the request
            body = json.loads(request.body)

            # Extract required fields
            tweet_id = body.get('tweet_id')
            updated_content = body.get('content')

            if not tweet_id or not updated_content:
                return JsonResponse({'error': 'Tweet ID and content are required'}, status=400)

            # Find the tweet to update
            try:
                tweet = Tweet.objects.get(id=tweet_id)
            except Tweet.DoesNotExist:
                return JsonResponse({'error': 'Tweet not found'}, status=404)

            # Update the tweet content
            tweet.content = updated_content

            # Extract mentions and trends from the updated content
            mentions = ', '.join(re.findall(r'@\w+', updated_content))
            trends = ', '.join(re.findall(r'#\w+', updated_content))
            tweet.mentions = mentions
            tweet.trends = trends
            tweet.save()

            # Return updated tweet data
            return JsonResponse({
                'message': 'Tweet updated successfully',
                'tweet': {
                    'id': tweet.id,
                    'content': tweet.content,
                    'mentions': tweet.mentions,
                    'trends': tweet.trends,
                    'created_at': tweet.created_at,
                    'updated_at': tweet.updated_at,
                    'person': {
                        'name': tweet.person.name,
                        'uservideo': tweet.person.uservideo,
                    }
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
@login_required
def retweet_view(request):
    if request.method == "POST":
        try:
            # Parse the JSON body from the request
            body = json.loads(request.body)

            # Extract required fields
            tweet_id = body.get('tweet_id')
            content = body.get('content', '')  # Optionally allow the user to add their own content

            if not tweet_id:
                return JsonResponse({'error': 'Tweet ID is required'}, status=400)

            # Find the tweet to retweet
            tweet = get_object_or_404(Tweet, id=tweet_id)

            # Get the Person object associated with the logged-in user
            person = get_object_or_404(Person, username=request.user.username)

            # Create a new Retweet object
            retweet = Retweet.objects.create(
                person=person,  # Current user's associated Person object
                original_tweet=tweet,  # Reference the original tweet
                content=content  # Optional content added by the user
            )

            # Return retweet data
            return JsonResponse({
                'message': 'Tweet retweeted successfully',
                'retweet': {
                    'id': retweet.id,
                    'content': retweet.content,
                    'created_at': retweet.created_at,
                    'person': {
                        'name': retweet.person.name,
                        'user_video': tweet.person_uservideo,
                        'username': retweet.person.username,
                    },
                    'original_tweet': {
                        'id': tweet.id,
                        'content': tweet.content,
                        'mentions': tweet.mentions,
                        'trends': tweet.trends,
                        'created_at': tweet.created_at,
                        'updated_at': tweet.updated_at,
                        'person': {
                            'name': tweet.person.name,
                            'username': tweet.person.username,
                            'user_video': tweet.person_uservideo  # Use `person_uservideo` property from Tweet
                        }
                    }
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
