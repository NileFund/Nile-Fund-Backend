from django.urls import path
from .views import ReportProjectView, ReportCommentView


urlpatterns = [

    path('projects/<int:project_id>/report/', ReportProjectView.as_view(), name='report-project'),
    path('comments/<int:comment_id>/report/', ReportCommentView.as_view(), name='report-comment')
]