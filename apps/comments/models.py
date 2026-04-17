from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimeStampedModel


class Comments(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )
    body = models.TextField()

    class Meta:
        db_table = 'comments_comment'
        indexes  = [models.Index(fields=['project', 'parent'])]

    def clean(self):
        if self.parent and self.parent.parent_id is not None:
            raise ValidationError('Replies to replies are not allowed.')

    def __str__(self):
        label = 'Reply' if self.parent_id else 'Comment'
        return f'{label} by {self.author.email} on "{self.project.title}"'