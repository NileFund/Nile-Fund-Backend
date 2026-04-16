from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.models import TimeStampedModel
from apps.common.validators import validate_not_in_past, validate_future_date


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'projects_tag'

    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        RUNNING   = 'running',   'Running'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    owner    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')

    title        = models.CharField(max_length=200)
    details      = models.TextField()
    total_target = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1, message='Target must be at least 1 EGP.')],
    )
    start_time   = models.DateTimeField(validators=[validate_not_in_past])
    end_time     = models.DateTimeField(validators=[validate_future_date])
    is_cancelled = models.BooleanField(default=False)
    is_featured  = models.BooleanField(default=False)

    class Meta:
        db_table = 'projects_project'
        indexes  = [
            models.Index(fields=['is_cancelled']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]

    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({'end_time': 'End time must be after start time.'})

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.is_cancelled:
            return self.Status.CANCELLED
        now = timezone.now()
        if now < self.start_time:
            return self.Status.PENDING
        if now <= self.end_time:
            return self.Status.RUNNING
        return self.Status.COMPLETED

    @property
    def total_donated(self):
        return self.donations.aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def donation_percentage(self):
        if not self.total_target:
            return 0
        return (self.total_donated / self.total_target) * 100

    @property
    def average_rating(self):
        return self.ratings.aggregate(avg=models.Avg('value'))['avg'] or 0


class ProjectPicture(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='pictures',
    )
    image = models.ImageField(upload_to='projects/')

    class Meta:
        db_table = 'projects_picture'

    def __str__(self):
        return f'Picture for "{self.project.title}"'
