from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Rating(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    value = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, message='Rating must be at least 1.'),
            MaxValueValidator(5, message='Rating cannot exceed 5.'),
        ],
    )

    class Meta:
        db_table        = 'ratings_rating'
        unique_together = [('project', 'user')]
        indexes         = [models.Index(fields=['project'])]

    def __str__(self):
        return f'{self.user.email} → "{self.project.title}": {self.value}/5'