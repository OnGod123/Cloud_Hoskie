from django.views import View
from django.http import JsonResponse
from myapp.profile.tweet.tweet_models import Tweet
import redis
import time
import logging
from django.db import DatabaseError

# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Setup logging
logger = logging.getLogger(__name__)

class TrendView(View):
    """
    A Django class-based view to handle trends and associated tweets.
    """

    def clear_redis_if_needed(self):
        """
        Clears the Redis database if 24 hours have passed since the last update.
        """
        try:
            last_updated = redis_client.get('trends_last_updated')
            if last_updated:
                last_updated = int(last_updated)
                current_time = int(time.time())
                # If 24 hours have passed (86400 seconds)
                if current_time - last_updated >= 86400:
                    redis_client.flushdb()  # Clears the entire Redis database
                    redis_client.set('trends_last_updated', current_time)  # Update the timestamp
            else:
                # If no timestamp is found, set it for the first time
                redis_client.set('trends_last_updated', int(time.time()))
        except redis.RedisError as e:
            logger.error(f"Redis error in clear_redis_if_needed: {e}")
            raise

    def process_trends(self):
        """
        Processes trends dynamically from all tweets in the database.
        This ensures Redis contains the most up-to-date ranking.
        """
        try:
            # First clear Redis data if needed
            self.clear_redis_if_needed()

            all_tweets = Tweet.objects.all().values("id", "trends")
            for tweet in all_tweets:
                self.process_trends(tweet["trends"], tweet["id"])
        except DatabaseError as e:
            logger.error(f"Database error in process_trends: {e}")
            raise
        except redis.RedisError as e:
            logger.error(f"Redis error in process_trends: {e}")
            raise

    def get(self, request, trend=None):
        """
        Handles GET requests to retrieve top trends or tweets associated with a specific trend.

        Args:
            request: The HTTP request object.
            trend (str, optional): A specific trend to fetch tweets for.

        Returns:
            JsonResponse: A JSON response containing trends or associated tweets.
        """
        try:
            # Update trend rankings in Redis dynamically
            self.process_trends()

            if not trend:
                # Fetch top trends from Redis
                top_trends = redis_client.zrevrange("trends_rank", 0, 9, withscores=True)
                trends_with_scores = [{"trend": t.decode(), "count": int(s)} for t, s in top_trends]
                return JsonResponse({"top_trends": trends_with_scores}, status=200)

            # Fetch tweets associated with the specific trend
            tweet_ids = redis_client.lrange(f"{trend}:tweets", 0, -1)
            tweets = Tweet.objects.filter(id__in=[int(tid) for tid in tweet_ids]).values(
                "id", "content", "trends", "person__name", "person__uservideo", "created_at"
            )

            return JsonResponse({"trend": trend, "tweets": list(tweets)}, status=200)

        except redis.RedisError as e:
            logger.error(f"Redis error in get method: {e}")
            return JsonResponse({"error": "Redis server is unavailable. Please try again later."}, status=503)

        except DatabaseError as e:
            logger.error(f"Database error in get method: {e}")
            return JsonResponse({"error": "Database error occurred. Please try again later."}, status=500)

        except Exception as e:
            logger.error(f"Unexpected error in get method: {e}")
            return JsonResponse({"error": "An unexpected error occurred. Please try again later."}, status=500)
