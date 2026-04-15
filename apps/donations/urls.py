from django.urls import path
from .views import DonationCreateView

urlpatterns = [
    path('donations/', DonationCreateView.as_view(), name='donation-create'),
]