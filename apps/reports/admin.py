
from django.contrib import admin
from .models import ProjectReport, CommentReport


@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ['project', 'reporter', 'reason', 'created_at']
    search_fields = ['project__title', 'reporter__email']
    list_filter = ['created_at']


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ['comment', 'reporter', 'reason', 'created_at']
    search_fields = ['reporter__email']
    list_filter = ['created_at']