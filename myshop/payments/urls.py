from django.urls import path
from .views import *



urlpatterns = [
    path('success_url/', success_esawa, name='success_payment'),
    path('failure_url/', failure_payment, name='failure_payment'),
]