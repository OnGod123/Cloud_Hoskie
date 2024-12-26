from django.urls import path
from . import views

urlpatterns = [
    # Other URLs for your app
    path('compare-face/', views.identify_person, name='compare_face'),
]
