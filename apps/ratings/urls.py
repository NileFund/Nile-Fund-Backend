from django.urls import path
from .views import (
    RatingCreateView,
    RatingUpdateView,
    ProjectRatingsListView,
    ProjectRatingSummaryView,
    TopRatedProjectsView,
    RecentRatingsView,
)
urlpatterns = [
    path('projects/<int:project_id>/ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('projects/<int:project_id>/ratings/update/', RatingUpdateView.as_view(), name='rating-update'),
    path('projects/<int:project_id>/ratings/list/', ProjectRatingsListView.as_view(), name='project-ratings'),
    path('projects/<int:project_id>/ratings/summary/', ProjectRatingSummaryView.as_view(), name='project-rating-summary'),
    path('top-rated/', TopRatedProjectsView.as_view(), name='top-rated-projects'),
    path('recent-rated/', RecentRatingsView.as_view(), name='recent-ratings'),
]