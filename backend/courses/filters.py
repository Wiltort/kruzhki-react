from django_filters.rest_framework import FilterSet, filters
from .models import Rubric, Stud_Group
from django.contrib.auth import get_user_model


User = get_user_model()

class RubricFilter(FilterSet):
    teacher = filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_staff=True))
    rubric = filters.ModelMultipleChoiceFilter(
        field_name='rubric__slug',
        queryset=Rubric.objects.all(),
        to_field_name='slug',
    )
    is_in_students = filters.BooleanFilter(method='get_is_in_students')
    is_teacher = filters.BooleanFilter(method='get_is_teacher')
    
    class Meta:
        model = Stud_Group
        fields = ('rubric', 'teacher', 'is_in_students', 'is_teacher')

    def get_is_in_students(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
                return queryset.filter(id = self.request.user.in_groups.id)
        return queryset
        
    def get_is_teacher(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True and self.request.user.is_staff is True:
            return queryset.filter(teacher=self.request.user)
        return queryset