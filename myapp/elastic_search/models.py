from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from myapp.profile.model_profile import Profile
from myapp.profile.Image.image_models import Image
from myapp.profile.tweet.tweet_models import Tweet
from myapp.profile.video.videos_model import Video

@registry.register_document
class ProfileDocument(Document):
    class Index:
        name = 'profiles'  # Index name for profiles

    class Django:
        model = Profile  # Link directly to the Profile model

        # Only index the fields that belong to the Profile model itself
        fields = [
            'id',                # UUIDField for the unique identifier
            'username',          # CharField for the username (unique)
            'user_video',        # URLField for the user's video URL
            'social_media_url',  # URLField for social media URL
            'bio',               # TextField for the bio
            'profile_picture',   # ImageField for the profile picture URL (or any other URLField)
            'created_at',        # DateTimeField for the creation timestamp
            'updated_at'         # DateTimeField for the update timestamp
        ]
        
    def prepare_username(self, instance):
        return instance.username  # Directly from the Profile model

    def prepare_user_video(self, instance):
        return instance.user_video  # Directly from the Profile model

    def prepare_social_media_url(self, instance):
        return instance.social_media_url  # Directly from the Profile model

    def prepare_bio(self, instance):
        return instance.bio  # Directly from the Profile model

    def prepare_profile_picture(self, instance):
        return instance.profile_picture.url if instance.profile_picture else None  # Handle image URL

    def prepare_created_at(self, instance):
        return instance.created_at  # Directly from the Profile model

    def prepare_updated_at(self, instance):
        return instance.updated_at  # Directly from the Profile model


@registry.register_document
class ImageDocument(Document):
    class Index:
        name = 'images'  # Index name for images

    class Django:
        model = Image  # Link directly to the Image model

        # Fields to index from the Image model itself
        fields = [
            'id',              # The primary key ID for Image model
            'image_file',      # ImageField for the image file URL
            'caption',         # CharField for the caption text
            'created_at',      # DateTimeField for the creation timestamp
            'updated_at'       # DateTimeField for the update timestamp
        ]

    def prepare_caption(self, instance):
        return instance.caption  # Direct field from the Image model

    def prepare_image_file(self, instance):
        return instance.image_file.url if instance.image_file else None  # URL of the image file

    def prepare_created_at(self, instance):
        return instance.created_at  # Direct field from Image model

    def prepare_updated_at(self, instance):
        return instance.updated_at  # Direct field from Image model


@registry.register_document
class VideoDocument(Document):
    class Index:
        name = 'videos'  # Index name for videos

    class Django:
        model = Video  # Link directly to the Video model

        # Fields to index from the Video model itself
        fields = [
            'id',               # UUIDField for the unique identifier
            'title',            # CharField for the video title
            'video_file',       # URLField or FileField for the video file URL
            'created_at',       # DateTimeField for creation timestamp
            'updated_at'        # DateTimeField for last update timestamp
        ]

    def prepare_title(self, instance):
        return instance.title  # Directly from the Video model

    def prepare_video_file(self, instance):
        return instance.video_file.url if instance.video_file else None  # URL of the video file

    def prepare_created_at(self, instance):
        return instance.created_at  # Directly from the Video model

    def prepare_updated_at(self, instance):
        return instance.updated_at  # Directly from the Video model


@registry.register_document
class TweetDocument(Document):
    class Index:
        name = 'tweets'  # Index name for tweets

    class Django:
        model = Tweet  # Link directly to the Tweet model

        # Fields to index from the Tweet model itself
        fields = [
            'id',              # UUIDField for the unique identifier
            'content',         # TextField for the tweet content
            'created_at',      # DateTimeField for the creation timestamp
            'updated_at'       # DateTimeField for the update timestamp
        ]

    def prepare_content(self, instance):
        return instance.content  # Direct field from the Tweet model

    def prepare_created_at(self, instance):
        return instance.created_at  # Direct field from the Tweet model

    def prepare_updated_at(self, instance):
        return instance.updated_at  # Direct field from the Tweet model
