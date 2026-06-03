import django_filters
from .models import Batch

class BatchFilter(django_filters.FilterSet):

    search = django_filters.CharFilter(method='custom_search')

    class Meta:
        model = Batch
        fields = []

    def custom_search(self, queryset, name, value):

        return queryset.filter(
            Q(batch_name__icontains=value) |
            Q(timing__icontains=value) |
            Q(course_name__icontains=value) |
            Q(trainer_name__icontains=value)
        )