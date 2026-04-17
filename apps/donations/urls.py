from django.urls import path
from .views import (
    DonationCreateView,
    DonationListView,
    DonationDetailView,
    MyDonationsView,
    ProjectDonationsView,
    ProjectDonationSummaryView,
    TopDonorsView,
    RecentDonationsView,
)

urlpatterns = [
    path('donations/', DonationCreateView.as_view(), name='donation-create'),
    path('donations/all/', DonationListView.as_view(), name='donation-list'),
    path('donations/<int:donation_id>/', DonationDetailView.as_view(), name='donation-detail'),
    path('donations/my/', MyDonationsView.as_view(), name='my-donations'),
    path('projects/<int:project_id>/donations/', ProjectDonationsView.as_view(), name='project-donations'),
    path('projects/<int:project_id>/donations/summary/', ProjectDonationSummaryView.as_view(), name='project-donation-summary'),
    path('projects/<int:project_id>/top-donors/', TopDonorsView.as_view(), name='top-donors'),
    path('donations/recent/', RecentDonationsView.as_view(), name='recent-donations'),
]