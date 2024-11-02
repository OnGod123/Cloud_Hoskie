from rest_framework import serializers
from myapp.models import Person
from .tweet.tweet_models import Tweet 
from .Image.image_models import Image
from .video.videos_model import Video  # Updated import path


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
