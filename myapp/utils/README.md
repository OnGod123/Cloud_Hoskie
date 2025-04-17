📦 Redis Caching Setup in Django
This project uses Redis as a caching backend via django-redis.

Requirements
Django 5.1.1

django-redis package installed

Redis server running locally on port 6379

Installation
Install Redis (if not already installed):

bash
Copy
Edit
sudo apt install redis-server
Install required Python package:

bash
Copy
Edit
pip install django-redis
Ensure Redis server is running:

bash
Copy
Edit
sudo service redis-server start
Django Configuration
In settings.py, configure caching:

python
Copy
Edit
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
✅ Important:

Do not override CACHES elsewhere in settings.py.

Ensure only one CACHES = {...} block exists.

Usage Example
To manually get a Redis connection in your Django app:

python
Copy
Edit
from django_redis import get_redis_connection

conn = get_redis_connection("default")
conn.set("mykey", "myvalue")
print(conn.get("mykey"))
✅ Common Issues
NotImplementedError: This backend does not support this feature
→ This happens if CACHES is incorrectly set or overwritten.

Could not create server TCP listening socket *:6379: bind: Address already in use
→ Redis is already running — no need to start a second server manually.

📖 References
django-redis GitHub

Django Cache Documentation

Would you like me to also generate a slightly fancier version with badges, like 🚀 Requirements | 🔥 Setup | 📚 Usage? (useful if you put it on GitHub) 🎯








