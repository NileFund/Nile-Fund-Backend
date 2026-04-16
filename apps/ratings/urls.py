from django.urls import path
from .views import (
    RatingCreateView,
    RatingUpdateView,
    ProjectRatingsListView,
)

urlpatterns = [
    path('projects/<int:project_id>/ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('projects/<int:project_id>/ratings/update/', RatingUpdateView.as_view(), name='rating-update'),
    path('projects/<int:project_id>/ratings/list/', ProjectRatingsListView.as_view(), name='project-ratings'),
]