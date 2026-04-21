import django_filters
from .models import Student

class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Student
        fields = ['name', 'id', 'mobile_no', 'email']