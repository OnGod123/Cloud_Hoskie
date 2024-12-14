from django.http import JsonResponse
from django.views.decorators.http import require_GET
from myapp.elastic_search.models import ProfileDocument
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
import json
from elasticsearch_dsl.connections import connections
from django.conf import settings
from elasticsearch import Elasticsearch
from Cloud_Hoskie.settings import ELASTICSEARCH_DSL, ELASTICSEARCH_EXTRA_PARAMS

def get_es_connection_from_settings():
    """
    Tries to connect to Elasticsearch using settings from the Django settings module.
    If the connection fails, it falls back to a direct connection with hardcoded credentials.
    """
    try:
        # Try connecting using settings from settings.py (elasticsearch_dsl)
        connections.configure(**ELASTICSEARCH_DSL['default'])
        
        # Create an Elasticsearch client from the configured connections
        es = connections.get_connection()
        
        # Check if the connection is successful
        if es.ping():
            print(f"Connected to Elasticsearch using settings as {ELASTICSEARCH_EXTRA_PARAMS['name']} (ID: {ELASTICSEARCH_EXTRA_PARAMS['id']}).")
            print(f"Encoded value: {ELASTICSEARCH_EXTRA_PARAMS['encoded']}")
            return es
        else:
            print("Failed to connect to Elasticsearch using settings.")
            return get_es_connection_fallback()  # Fallback to the direct connection

    except (AuthenticationException, ConnectionError) as e:
        # Catch authentication or connection errors and fall back to the direct connection
        print(f"Error while connecting using settings: {str(e)}")
        return get_es_connection_fallback()

    except Exception as e:
        print(f"Unexpected error while connecting using settings: {str(e)}")
        return get_es_connection_fallback()


def get_es_connection_fallback():
    """
    Fallback connection to Elasticsearch when the primary connection fails.
    Uses hardcoded credentials for the fallback connection.
    """
    try:
        # Fallback to direct Elasticsearch connection (using hardcoded credentials)
        es =  Elasticsearch(
            ['http://localhost:9200'],  # Localhost connection
           timeout=30  # Adjust the timeout if needed
          )

        # Check if the connection is successful
        if es.ping():
            print(f"Connected to Elasticsearch using fallback as {ELASTICSEARCH_EXTRA_PARAMS['name']} (ID: {ELASTICSEARCH_EXTRA_PARAMS['id']}).")
            print(f"Encoded value: {ELASTICSEARCH_EXTRA_PARAMS['encoded']}")
            return es
        else:
            print("Failed to connect to Elasticsearch using fallback.")
            return None

    except Exception as e:
        print(f"Error connecting to Elasticsearch using fallback: {str(e)}")
        return None




    
# Function to perform the autocomplete search
def autocomplete_username_search(username_input, page_size=10):
    # Try to get the connection from settings
    es = get_es_connection_from_settings()

    # If the connection from settings failed, try the fallback method
    if es is None:
        print("Falling back to direct connection...")
        es = get_es_connection_fallback()

    if es is None:
        return JsonResponse({"error": "Unable to connect to Elasticsearch."}, status=500)

    try:
        # Create the search query for Elasticsearch
        search_body = {
            "query": {
                "match": {
                    "username": username_input
                }
            },
            "size": page_size
        }

        # Perform the search
        response = es.search(index="profiles", body=search_body)

        # Parse and return results
        results = []
        for hit in response['hits']['hits']:
            results.append({
                "username": hit['_source'].get('username', ''),
                "social_media_url": hit['_source'].get('social_media_url', ''),
                "user_video": hit['_source'].get('user_video', ''),
            })
        
        return JsonResponse({"results": results})

    except AuthenticationException as e:
        return JsonResponse({"error": f"Authentication error: {str(e)}"}, status=401)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


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


# Other autocomplete methods (for videos, tweets, etc.)
@require_POST
def autocomplete_video(request):
    return autocomplete_response(request, autocomplete_video_search)

@require_POST
def autocomplete_tweet(request):
    return autocomplete_response(request, autocomplete_tweet_search)

@require_POST
def autocomplete_image(request):
    return autocomplete_response(request, autocomplete_image_search)
