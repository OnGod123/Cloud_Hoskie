import re
import logging
import redis
import time
from django.db import DatabaseError
from django.http import JsonResponse
from django.views import View
from myapp.profile.tweet.tweet_models import Tweet


# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Setup logging
logger = logging.getLogger(__name__)

class MentionView(View):
    """
    A Django class-based view to handle mentions and associated tweets.
    """

    def clear_redis_if_needed(self):
        """
        Clears the Redis database if 24 hours have passed since the last update.
        """
        try:
            last_updated = redis_client.get('mentions_last_updated')
            if last_updated:
                last_updated = int(last_updated)
                current_time = int(time.time())
                # If 24 hours have passed (86400 seconds)
                if current_time - last_updated >= 86400:
                    redis_client.flushdb()  # Clears the entire Redis database
                    redis_client.set('mentions_last_updated', current_time)  # Update the timestamp
            else:
                # If no timestamp is found, set it for the first time
                redis_client.set('mentions_last_updated', int(time.time()))
        except redis.RedisError as e:
            logger.error(f"Redis error in clear_redis_if_needed: {e}")
            raise

    def process_mentions(self):
        """
        Processes mentions dynamically from all tweets in the database.
        This ensures Redis contains the most up-to-date ranking of mentions.
        """
        try:
            # First clear Redis data if needed
            self.clear_redis_if_needed()

            all_tweets = Tweet.objects.all().values("id", "mentions")
            for tweet in all_tweets:
                mentions = tweet["mentions"]
                if mentions:
                    for mention in mentions.split(", "):  # Assuming multiple mentions are stored as comma-separated
                        self.process_mention(mention, tweet["id"])
        except DatabaseError as e:
            logger.error(f"Database error in process_mentions: {e}")
            raise
        except redis.RedisError as e:
            logger.error(f"Redis error in process_mentions: {e}")
            raise

    def process_mention(self, mention, tweet_id):
        """
        Processes each mention and stores it in Redis.
        """
        redis_client.lpush(f"mention:{mention}:tweets", tweet_id)

    def get(self, request, mention=None):
        """
        Handles GET requests to retrieve top mentions or tweets associated with a specific mention.

        Args:
            request: The HTTP request object.
            mention (str, optional): A specific mention to fetch tweets for.

        Returns:
            JsonResponse: A JSON response containing mentions or associated tweets.
        """
        try:
            # Update mention data in Redis dynamically
            self.process_mentions()

            if not mention:
                # Fetch top mentions from Redis
                top_mentions = redis_client.zrevrange("mentions_rank", 0, 9, withscores=True)
                mentions_with_scores = [{"mention": m.decode(), "count": int(s)} for m, s in top_mentions]
                return JsonResponse({"top_mentions": mentions_with_scores}, status=200)

            # Fetch tweets associated with the specific mention
            tweet_ids = redis_client.lrange(f"mention:{mention}:tweets", 0, -1)
            tweets = Tweet.objects.filter(id__in=[int(tid) for tid in tweet_ids]).values(
                "id", "content", "mentions", "person__name", "person__uservideo", "created_at"
            )

            return JsonResponse({"mention": mention, "tweets": list(tweets)}, status=200)

        except redis.RedisError as e:
            logger.error(f"Redis error in get method: {e}")
            return JsonResponse({"error": "Redis server is unavailable. Please try again later."}, status=503)

        except DatabaseError as e:
            logger.error(f"Database error in get method: {e}")
            return JsonResponse({"error": "Database error occurred. Please try again later."}, status=500)

        except Exception as e:
            logger.error(f"Unexpected error in get method: {e}")
            return JsonResponse({"error": "An unexpected error occurred. Please try again later."}, status=500)
