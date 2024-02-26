from django_filters.rest_framework import FilterSet, filters
from .models import Rubric, Stud_Group, Attending
from users.models import User
from django.utils import timezone


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
    not_beginned = filters.BooleanFilter(method='get_not_beginned')
    
    class Meta:
        model = Stud_Group
        fields = ('rubric', 'teacher', 'is_in_students', 'is_teacher', 'begin_at')

    def get_is_in_students(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
                return queryset.filter(id = self.request.user.in_groups.id)
        return queryset
        
    def get_is_teacher(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True and self.request.user.is_staff is True:
            return queryset.filter(teacher=self.request.user)
        return queryset
    
    def get_not_beginned(self, queryset, name, value):
         if value is True:
              return queryset.filter(begin_at__gte=timezone.now())
         return queryset
    

class AttendingFilter(FilterSet):
    stud_group = filters.ModelChoiceFilter(
        queryset=Stud_Group.objects.all(),
        field_name='lesson__stud_group'
    )
    period = filters.DateFromToRangeFilter(field_name='lesson__ldate')
    student = filters.ModelChoiceFilter(User.objects.filter(is_staff=False))
    my = filters.BooleanFilter(method='get_is_in_students')

    class Meta:
         model = Attending
         fields = ('stud_group', 'period', 'student', 'my')
    
    def get_is_in_students(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
                return queryset.filter(id = self.request.user.attending.id)
        return queryset