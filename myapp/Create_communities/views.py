from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Community, Tweet, Person
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators      import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CommunityView(View):
    def get(self, request, community_id=None):
        if community_id:
            try:
                community = Community.objects.get(id=community_id)
                members = [{'id': member.id, 'name': member.name} for member in community.members.all()]
                response_data = {'id': community.id, 'name': community.name, 'description': community.description, 'members': members}
                return JsonResponse(response_data)
            except Community.DoesNotExist:
                return JsonResponse({'error': 'Community not found'}, status=404)
        else:
            communities = Community.objects.all().values('id', 'name', 'description')
            return JsonResponse(list(communities), safe=False)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        try:
            community = Community.objects.create(name=data['name'], description=data.get('description', ''))
            return JsonResponse({'id': community.id, 'name': community.name, 'description': community.description})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    def post_member(self, request, community_id, person_id):
        try:
            community = Community.objects.get(id=community_id)
            person = Person.objects.get(id=person_id)
            community.add_member(person)
            return JsonResponse({'message': 'Member added successfully'})
        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
        except Person.DoesNotExist:
            return JsonResponse({'error': 'Person not found'}, status=404)
from .models import Comment


@method_decorator(csrf_exempt, name='dispatch')
class CommentView(View):
    def post(self, request, community_id, tweet_id):
        """
        POST: Add a comment to a tweet in a community.
        Only accessible to group members and valid tweets within the community.
        """
        try:
            community = Community.objects.get(id=community_id)

            # Check if the user is a community member
            user = request.user
            if not community.members.filter(id=user.id).exists():
                return HttpResponseForbidden("You are not a member of this community.")

            # Verify the tweet exists and belongs to the community
            try:
                tweet = Tweet.objects.get(id=tweet_id)
            except Tweet.DoesNotExist:
                return JsonResponse({'error': 'Tweet not found'}, status=404)

            if not tweet.person in community.members.all():
                return JsonResponse({'error': 'Tweet is not part of this community'}, status=403)

            # Create the comment
            data = json.loads(request.body.decode('utf-8'))
            content = data.get('content', '')
            comment = Comment.objects.create(tweet=tweet, person=user, content=content)

            return JsonResponse({
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

method_decorator(csrf_exempt, name='dispatch')
class RetweetView(View):
    def get(self, request, community_id):
        """
        GET: Retrieve all retweets for a specific community.
        Only accessible to group members.
        """
        try:
            community = Community.objects.get(id=community_id)

            # Check if the user is a community member
            user = request.user
            if not community.members.filter(id=user.id).exists():
                return HttpResponseForbidden("You are not a member of this community.")

            # Retrieve retweets for tweets by community members
            retweets = Retweet.objects.filter(original_tweet__person__in=community.members.all()).select_related('person', 'original_tweet')
            response_data = [
                {
                    'id': retweet.id,
                    'content': retweet.content,
                    'original_tweet': {
                        'id': retweet.original_tweet.id,
                        'content': retweet.original_tweet.content,
                        'person': {
                            'id': retweet.original_tweet.person.id,
                            'name': retweet.original_tweet.person.name
                        }
                    },
                    'person': {
                        'id': retweet.person.id,
                        'name': retweet.person.name
                    },
                    'created_at': retweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for retweet in retweets
            ]
            return JsonResponse(response_data, safe=False)

        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)

    def post(self, request, community_id):
        """
        POST: Create a retweet for a given tweet in a community.
        Only accessible to group members.
        """
        try:
            community = Community.objects.get(id=community_id)

            # Check if the user is a community member
            user = request.user
            if not community.members.filter(id=user.id).exists():
                return HttpResponseForbidden("You are not a member of this community.")

            # Create the retweet
            data = json.loads(request.body.decode('utf-8'))
            original_tweet_id = data.get('original_tweet_id')
            content = data.get('content', '')

            # Check if the original tweet exists
            try:
                original_tweet = Tweet.objects.get(id=original_tweet_id)
            except Tweet.DoesNotExist:
                return JsonResponse({'error': 'Original tweet not found'}, status=404)

            # Verify that the tweet belongs to the community
            if not original_tweet.person in community.members.all():
                return JsonResponse({'error': 'Tweet is not part of this community'}, status=403)

            # Create a retweet
            retweet = Retweet.objects.create(person=user, original_tweet=original_tweet, content=content)
            return JsonResponse({
                'id': retweet.id,
                'content': retweet.content,
                'original_tweet': {
                    'id': retweet.original_tweet.id,
                    'content': retweet.original_tweet.content
                },
                'created_at': retweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Community, Tweet, Person



@method_decorator(csrf_exempt, name='dispatch')
class TweetView(View):
    def get(self, request, community_id):
        """
        GET: Retrieve all tweets for a specific community.
        Only accessible to members of the community.
        """
        try:
            community = Community.objects.get(id=community_id)

            # Check if the user is a member of the community
            user = request.user
            if not community.members.filter(id=user.id).exists():
                return HttpResponseForbidden("You are not a member of this community.")

            # Retrieve all tweets within the community
            tweets = Tweet.objects.filter(person__in=community.members.all()).select_related('person')
            response_data = [
                {
                    'id': tweet.id,
                    'person': {
                        'id': tweet.person.id,
                        'name': tweet.person.name
                    },
                    'content': tweet.content,
                    'mentions': tweet.mentions,
                    'trends': tweet.trends,
                    'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for tweet in tweets
            ]
            return JsonResponse(response_data, safe=False)

        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)

    def post(self, request, community_id):
        """
        POST: Create a new tweet for a specific community.
        Only accessible to members of the community.
        """
        try:
            community = Community.objects.get(id=community_id)

            # Check if the user is a member of the community
            user = request.user
            if not community.members.filter(id=user.id).exists():
                return HttpResponseForbidden("You are not a member of this community.")

            # Create the tweet
            data = json.loads(request.body.decode('utf-8'))
            content = data.get('content', '')
            mentions = data.get('mentions', '')
            trends = data.get('trends', '')
            tweet = Tweet.objects.create(person=user, content=content, mentions=mentions, trends=trends)
            return JsonResponse({
                'id': tweet.id,
                'content': tweet.content,
                'mentions': tweet.mentions,
                'trends': tweet.trends,
                'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        except Community.DoesNotExist:
            return JsonResponse({'error': 'Community not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Video, Tweet, Like, Community


# Video like view
@method_decorator(csrf_exempt, name='dispatch')
class VideoLikeView(View):
    def post(self, request, video_id, community_id):
        # Get the community and video instance
        community = get_object_or_404(Community, id=community_id)
        video = get_object_or_404(Video, id=video_id)

        # Ensure the current user is a member of the community
        if request.user not in community.members.all():
            return HttpResponse("You are not a member of this community.", status=403)

        # Check if the user has already liked the video
        if Like.objects.filter(person=request.user.person, video=video, community=community).exists():
            return HttpResponse("You have already liked this video.", status=400)

        # Create a like instance
        like = Like(person=request.user.person, video=video, community=community)
        like.save()

        return redirect('community_videos', community_id=community.id)  # Redirect to community's video list


# Tweet like view
@method_decorator(csrf_exempt, name='dispatch')
class TweetLikeView(View):
    def post(self, request, tweet_id, community_id):
        # Get the community and tweet instance
        community = get_object_or_404(Community, id=community_id)
        tweet = get_object_or_404(Tweet, id=tweet_id)

        # Ensure the current user is a member of the community
        if request.user not in community.members.all():
            return HttpResponse("You are not a member of this community.", status=403)

        # Check if the user has already liked the tweet
        if Like.objects.filter(person=request.user.person, tweet=tweet, community=community).exists():
            return HttpResponse("You have already liked this tweet.", status=400)

        # Create a like instance
        like = Like(person=request.user.person, tweet=tweet, community=community)
        like.save()

        return redirect('community_tweets', community_id=community.id)  # Redirect to community's tweet list
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Video, Community


# Video upload view using class-based view
@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(View):
    def get(self, request, community_id):
        # Get the community instance
        community = get_object_or_404(Community, id=community_id)

        # Ensure the current user is a member of the community
        if request.user not in community.members.all():
            return HttpResponse("You are not a member of this community.", status=403)

        # Render the video upload form
        form = Video()
        return render(request, 'upload_video.html', {'form': form, 'community': community})

    def post(self, request, community_id):
        # Get the community instance
        community = get_object_or_404(Community, id=community_id)

        # Ensure the current user is a member of the community
        if request.user not in community.members.all():
            return HttpResponse("You are not a member of this community.", status=403)

        # Handle video upload
        form = Video(request.POST, request.FILES)
        if form.is_valid():
            # Create the video instance and associate it with the current user and community
            video = form.save(commit=False)
            video.person = request.user.person  # Assuming user has a related Person object
            video.community = community
            video.save()
            return redirect('community_videos', community_id=community.id)  # Redirect to community video list

        return render(request, 'upload_video.html', {'form': form, 'community': community})

# Community video list view using class-based view
@method_decorator(csrf_exempt, name='dispatch')
class CommunityVideosView(View):
    def get(self, request, community_id):
        # Get the community instance
        community = get_object_or_404(Community, id=community_id)

        # Ensure the current user is a member of the community
        if request.user not in community.members.all():
            return HttpResponse("You are not a member of this community.", status=403)

        # Get all videos shared within the community
        videos = Video.objects.filter(community=community)
        return render(request, 'community_videos.html', {'videos': videos, 'community': community})
