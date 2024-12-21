from django.urls import path
from .views import follow_view

urlpatterns = [
    path('persons/<int:person_id>/follow/', follow_view, name='follow_view'),
]
