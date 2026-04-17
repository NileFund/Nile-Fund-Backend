import django_filters
from .models import Rating


class RatingFilter(django_filters.FilterSet):
    min_value = django_filters.NumberFilter(field_name="value", lookup_expr='gte')
    max_value = django_filters.NumberFilter(field_name="value", lookup_expr='lte')

    user = django_filters.NumberFilter(field_name="user__id")
    project = django_filters.NumberFilter(field_name="project__id")

    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Rating
        fields = ['project', 'user', 'min_value', 'max_value']