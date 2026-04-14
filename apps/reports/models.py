from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class ProjectReport(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='reports',
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_reports',
    )
    reason = models.TextField(blank=True)

    class Meta:
        db_table        = 'reports_project_report'
        unique_together = [('project', 'reporter')]

    def __str__(self):
        return f'{self.reporter.email} reported "{self.project.title}"'


class CommentReport(TimeStampedModel):
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        related_name='reports',
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_reports',
    )
    reason = models.TextField(blank=True)

    class Meta:
        db_table        = 'reports_comment_report'
        unique_together = [('comment', 'reporter')]

    def __str__(self):
        return f'{self.reporter.email} reported comment #{self.comment.id}'