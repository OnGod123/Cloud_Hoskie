from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from myapp.models import Person 
from myapp.profile.tweet.tweet_models import Tweet  
from myapp.profile.Image.image_models import Image  # Fixed import statement
from myapp.profile.video.videos_model import Video  
from .model_profile import Profile
import geocoder

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ip_location(ip):
    cache_key = f"location_{ip}"
    location_data = cache.get(cache_key)

    if not location_data:
        g = geocoder.ip(ip)
        if g.ok:
            location_data = {'ip': ip, 'country': g.country}
            cache.set(cache_key, location_data, timeout=60 * 60)
        else:
            location_data = {'error': 'Unable to locate IP'}

    return location_data

class ProfilePagination(PageNumberPagination):
    page_size = 10  # Set the default number of profiles per page
    page_size_query_param = 'page_size'  # Allow clients to set page size
    max_page_size = 100  # Limit the maximum page size

@api_view(['GET'])
def all_user_profiles(request):
    # Check if cached data exists
    cache_key = 'all_user_profiles'
    cached_profiles = cache.get(cache_key)

    if cached_profiles is not None:
        return Response(cached_profiles)

    paginator = ProfilePagination()
    profiles = Profile.objects.prefetch_related('person__tweet_set', 'person__image_set', 'person__video_set')  # Optimize queries
    page = paginator.paginate_queryset(profiles, request)
    response_data = []

    for profile in page:
        # Get the user video from the Profile instance
        user_video = profile.user_video.url if profile.user_video else None
        
        # Fetch related tweets and images
        tweets = Tweet.objects.filter(person=profile.person).values()  # Fetch all fields for tweets
        images = Image.objects.filter(person=profile.person).values()  # Fetch all fields for images
        
        # Fetch all videos related to the Person
        person_videos = Video.objects.filter(person=profile.person).values()  # Videos related to the person

        profile_data = {
            'username': profile.username,
            'social_media_url': profile.social_media_url,
            'bio': profile.bio,
            'user_video': user_video,  # Profile's user video
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'videos': list(person_videos),  # List of videos from the Video table
            'tweets': list(tweets),  # Convert to list
            'images': list(images),  # Convert to list
        }

        response_data.append(profile_data)

    # Cache the response for future requests
    cache.set(cache_key, response_data, timeout=60 * 15)  # Cache for 15 minutes

    return paginator.get_paginated_response(response_data)

@api_view(['GET'])
def user_profile_by_username(request, username):
    cache_key = f'user_profile_{username}'
    cached_profile = cache.get(cache_key)

    if cached_profile is not None:
        return Response(cached_profile)

    profile = get_object_or_404(Profile.objects.select_related('person'), username=username)
    
    # Fetch user's tweets and images with all fields
    tweets = Tweet.objects.filter(person=profile.person).values()
    images = Image.objects.filter(person=profile.person).values()

    # Get user video from the Profile
    user_video = profile.user_video.url if profile.user_video else None

    # Fetch all videos related to the Person
    person_videos = Video.objects.filter(person=profile.person).values()  # Videos related to the person

    data = {
        'username': profile.username,
        'social_media_url': profile.social_media_url,
        'bio': profile.bio,
        'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
        'user_video': user_video,  # Profile's user video
        'videos': list(person_videos),  # List of videos from the Video table
        'tweets': list(tweets),  # Convert to list
        'images': list(images),  # Convert to list
    }

    # Cache the profile response
    cache.set(cache_key, data, timeout=60 * 15)  # Cache for 15 minutes

    return Response(data)

@api_view(['POST'])
def update_profile(request, username):
    profile = get_object_or_404(Profile, username=username)

    if request.method == 'POST':
        # Extract data from request
        bio = request.data.get('bio', profile.bio)
        user_video = request.data.get('user_video', profile.user_video)
        profile_picture = request.FILES.get('profile_picture', profile.profile_picture)

        # Update only the fields that are being changed
        if bio is not None:  # Allow empty strings
            profile.bio = bio
        if user_video is not None:  # Allow empty strings
            profile.user_video = user_video
        if profile_picture is not None:  # Allow removing the image
            profile.profile_picture = profile_picture

        # Save the profile without updating username or social media URL
        profile.save()

        # Clear the cache for this profile
        cache_key = f'user_profile_{username}'
        cache.delete(cache_key)

        return JsonResponse({
            'message': 'Profile updated successfully',
            'profile': {
                'username': profile.username,
                'social_media_url': profile.social_media_url,
                'bio': profile.bio,
                'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                'user_video': profile.user_video.url if profile.user_video else None  # Profile's user video
            }
        }, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def serve_profile_view(request, profile_id):
    client_ip = get_client_ip(request)
    location_data = get_ip_location(client_ip)

    if 'error' in location_data:
        return JsonResponse({'error': location_data['error']}, status=400)

    # Check if the IP has recently accessed the profile
    cache_key = f"viewed_profile_{client_ip}_{profile_id}"
    if cache.get(cache_key):
        return all_user_profiles(request)  # Serve all profiles if the same IP accessed recently

    # Cache this profile view for the IP
    cache.set(cache_key, True, timeout=10 * 60)  # Cache for 10 minutes

    # Serve specific profile view if not cached
    return user_profile_by_username(request, profile_id)
