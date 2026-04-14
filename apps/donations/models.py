from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Donation(TimeStampedModel):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.PROTECT,      
        related_name='donations',
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='donations',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, message='Donation must be at least 1 EGP.')],
    )

    class Meta:
        db_table = 'donations_donation'
        indexes  = [models.Index(fields=['project'])]

    def clean(self):
        from apps.projects.models import Project
        if self.project.status != Project.Status.RUNNING:
            raise ValidationError('You can only donate to running projects.')

    def __str__(self):
        return f'{self.donor.email} → "{self.project.title}": {self.amount} EGP'