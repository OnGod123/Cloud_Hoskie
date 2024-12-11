from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Tweet
from myapp.models import Person

# This view handles both GET and POST requests for the tweet submission form
def tweet_view(request):
    if request.method == "GET":
        # Render the form HTML for submitting a tweet
        return render(request, 'tweet_form.html')

    elif request.method == "POST":
        # Handle tweet submission
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)

        # Ensure 'person_id' is provided and is a valid integer
        person_id = request.POST.get('person_id')
        if not person_id or not person_id.isdigit():
            return JsonResponse({'error': 'Valid person_id is required'}, status=400)

        # Retrieve the person from the database
        try:
            person = Person.objects.get(id=person_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Person not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error retrieving person: {str(e)}'}, status=500)

        # Optional fields: mentions and trends
        mentions = request.POST.get('mentions', '')  # e.g. "@ahmed, @john"
        trends = request.POST.get('trends', '')  # e.g. "#olympic, #sports"

        # Save the tweet in the database
        try:
            tweet = Tweet.objects.create(
                person=person,
                content=content,
                mentions=mentions,
                trends=trends
            )
        except Exception as e:
            return JsonResponse({'error': f'Error saving tweet: {str(e)}'}, status=500)

        # Success response
        return JsonResponse({'message': 'Tweet created successfully', 'tweet_id': tweet.id})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
