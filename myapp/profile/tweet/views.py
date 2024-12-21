from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import re

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
