import django_filters
from django.db.models import Q
from .models import Student

class StudentFilter(django_filters.FilterSet):

    search = django_filters.CharFilter(method='custom_search', label='Search')

    course = django_filters.CharFilter(
        field_name='enrollments__course__course',
        lookup_expr='icontains',
        label='Course'
    )

    batch = django_filters.CharFilter(
        field_name='enrollments__batch',
        lookup_expr='icontains',
        label='Batch'
    )

    class Meta:
        model = Student
        fields = ['search', 'course', 'batch']

    def custom_search(self, queryset, name, value):
        terms = value.split()
        query = Q()

        for term in terms:
            query &= (
                Q(First_name__icontains=term) |
                Q(Last_name__icontains=term)
            )

        return queryset.filter(query)