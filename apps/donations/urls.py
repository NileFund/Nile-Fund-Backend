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
    path('', DonationCreateView.as_view(), name='donation-create'),
    path('all/', DonationListView.as_view(), name='donation-list'),
    path('my/', MyDonationsView.as_view(), name='my-donations'),        # ← move up
    path('recent/', RecentDonationsView.as_view(), name='recent-donations'),  # ← move up
    path('<int:donation_id>/', DonationDetailView.as_view(), name='donation-detail'),
    
    #path('projects/<int:project_id>/donations/', ProjectDonationsView.as_view(), name='project-donations'),
    #path('projects/<int:project_id>/donations/summary/', ProjectDonationSummaryView.as_view(), name='project-donation-summary'),
    #path('projects/<int:project_id>/top-donors/', TopDonorsView.as_view(), name='top-donors'),
]