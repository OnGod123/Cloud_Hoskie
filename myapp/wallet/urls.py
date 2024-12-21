from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<str:payment_type>/', views.initiate_payment, name='initiate_payment'),
]
