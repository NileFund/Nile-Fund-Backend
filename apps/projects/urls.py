from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.ProjectViewSet, basename='projects')

urlpatterns = [
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('', include(router.urls)),
]
