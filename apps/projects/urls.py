from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from apps.donations.views import ProjectDonationsView, ProjectDonationSummaryView, TopDonorsView

router = DefaultRouter()
router.register('', views.ProjectViewSet, basename='projects')

urlpatterns = [
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('', include(router.urls)),
    path('<int:project_id>/donations/', ProjectDonationsView.as_view()),
    path('<int:project_id>/donations/summary/', ProjectDonationSummaryView.as_view()),
    path('<int:project_id>/top-donors/', TopDonorsView.as_view()),
]
