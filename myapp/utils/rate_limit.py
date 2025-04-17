# myapp/utils/rate_limit.py

import logging
from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def rate_limit_view(limit=None, window=None, prefix="rl"):
    """
    Decorator to rate-limit a view by client IP.
    :param limit: Max requests per window (default from settings.RATE_LIMIT)
    :param window: Window size in seconds (default from settings.RATE_LIMIT_WINDOW)
    :param prefix: Key namespace in Redis
    """
    limit = limit or getattr(settings, "RATE_LIMIT", 50)
    window = window or getattr(settings, "RATE_LIMIT_WINDOW", 60)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # grab the redis client *now* (when Django is fully set up)
            redis_client = get_redis_connection("default")

            ip = (
                request.META.get("HTTP_X_FORWARDED_FOR", "")
                .split(",")[0]
                .strip()
                or request.META.get("REMOTE_ADDR", "")
            )
            key = f"{prefix}:{ip}"

            try:
                # increment & set TTL
                count = redis_client.incr(key)
                if count == 1:
                    redis_client.expire(key, window)
                ttl = redis_client.ttl(key)
            except Exception:
                logger.exception("Redis error in rate_limit_view")
                return view_func(request, *args, **kwargs)

            if count > limit:
                retry_after = ttl if ttl and ttl > 0 else window
                return JsonResponse(
                    {"detail": "Too Many Requests, please try again later."},
                    status=429,
                    headers={"Retry-After": str(retry_after)},
                )

            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator

