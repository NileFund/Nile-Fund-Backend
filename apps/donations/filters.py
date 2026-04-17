import django_filters
from .models import Donation

class DonationFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')

    project = django_filters.NumberFilter(field_name="project__id")
    donor = django_filters.NumberFilter(field_name="donor__id")

    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date   = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    donor_email = django_filters.CharFilter(field_name="donor__email", lookup_expr='icontains')

    class Meta:
        model = Donation
        fields = []    