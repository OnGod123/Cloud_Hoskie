from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, Tweet, Image

@api_view(['GET'])
def all_user_profiles(request):
    
    profiles = Profile.objects.all()
    
    response_data = []

    for profile in profiles:
        
        user_id = profile.person.id

        
        tweets = Tweet.objects.filter(person__id=user_id).values('content', 'created_at')

        
        images = Image.objects.filter(person__id=user_id).values('image_file', 'caption', 'created_at')

        
       	user_video = profile.user_video

        
        profile_data = {
            'username': profile.username,
            'social_media_url': profile.social_media_url,
            'bio': profile.bio,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'videos': user_video,
            'tweets': list(tweets),
            'images': list(images),
        }
        
        response_data.append(profile_data)
    
    return Response(response_data)

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, Tweet, Image

@api_view(['GET'])
def user_profile_by_username(request, username):
    try:
        # Get the user's profile using the username
        profile = Profile.objects.get(username=username)

        # Get the user's ID from the profile
        user_id = profile.person.id  # Assuming 'person' is the ForeignKey to Person model

        # Fetch user's tweets
        tweets = Tweet.objects.filter(person__id=user_id).values('content', 'created_at')

        # Fetch user's images
        images = Image.objects.filter(person__id=user_id).values('image_file', 'caption', 'created_at')

        # Get user video
        user_video = profile.user_video
        
        # Construct the response data
        data = {
            'username': profile.username,
            'social_media_url': profile.social_media_url,
            'bio': profile.bio,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'videos': user_video,
            'tweets': list(tweets),
            'images': list(images),
        }
        
        return Response(data)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

