from django.db import models

from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
 
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon        = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        help_text='Optional icon shown on the homepage category list'
    )

    class Meta:
        db_table      = 'categories_category'
        verbose_name_plural = 'categories'
        ordering      = ['name']

    def __str__(self):
        return self.name