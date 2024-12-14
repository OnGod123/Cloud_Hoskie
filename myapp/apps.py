from django.apps import AppConfig
from .elasticsearch_config import configure_elasticsearch

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        configure_elasticsearch()