from django.http import JsonResponse
from django.views.decorators.http import require_GET
from myapp.elastic_search.models import ProfileDocument
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
import json

@require_GET
def get_profiles(request):
    """
    Django view for handling GET requests to fetch profiles by username input.
    Renders the search page and returns the search results in JSON format.
    """
    # If the request is to render the search page
    if request.GET.get('username_input') is None:
        return render(request, 'search.html')  # This will render search.html for the root URL

    # Otherwise, handle the autocomplete logic
    username_input = request.GET.get('username_input', "")
    page_size = int(request.GET.get("page_size", 10))  # Default page size is 10

    # Collect autocomplete results with only specific fields
    results = []
    for batch in autocomplete_username_search(username_input, page_size=page_size):
        results.extend(batch)  # Append each batch of filtered results

    # Return results as JSON
    return JsonResponse({"results": results})

def autocomplete_username_search(username_input, page_size=10):
    """
    Autocomplete search for profiles by username, yielding only a limited number of results at a time.
    
    :param username_input: The input string typed by the user (e.g., "@jo")
    :param page_size: Number of results to yield at a time (default is 10)
    """
    # Remove "@" if it's included in the input
    username_input = username_input.lstrip("@")

    offset = 0
    while True:
        # Build the query to match usernames progressively as input length increases
        query = ProfileDocument.search() \
            .query("match_phrase_prefix", username=username_input) \
            .sort("username") \
            .extra(size=page_size, from_=offset)
        
        results = query.execute()

        # If no more results, break out of the loop
        if not results:
            break
        
        # Yield each user profile as a dictionary containing only the required fields
        for result in results:
            user_data = {
                "username": result.username,
                "user_video": result.user_video,
                "social_media_url": result.social_media_url
            }
            yield user_data

        # Increase the offset for the next batch of results
        offset += page_size
def autocomplete_profile(request):
    return autocomplete_response(request, autocomplete_profile_search)

# Autocomplete for videos
@require_POST
def autocomplete_video(request):
    return autocomplete_response(request, autocomplete_video_search)

# Autocomplete for tweets
@require_POST
def autocomplete_tweet(request):
    return autocomplete_response(request, autocomplete_tweet_search)

# Autocomplete for images
@require_POST
def autocomplete_image(request):
    return autocomplete_response(request, autocomplete_image_search)
