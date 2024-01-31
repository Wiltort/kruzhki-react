from rest_framework import serializers
from .models import Rubric, Stud_Group, Student, Lesson, Schedule, Attending
from rest_framework.validators import UniqueTogetherValidator


class ScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Schedule
        fields = ('id', 'group', 'day_of_week', 'duration', 'begin_at')


class AttendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attending
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)

    class Meta:
        model = Lesson
        fields = ('id', 'stud_group', 'date', 'topic', 'attending')


class StudentSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)
    
    class Meta:
        model = Student
        fields = ('id', 'user', 'in_group', 'attending')
        validators = [
            UniqueTogetherValidator(
                queryset=Student.objects.all(),
                fields = ['user', 'in_group']
            )
        ]

class Stud_GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many = True, read_only = True)
    lessons = LessonSerializer(many = True, read_only = True)
    schedule = ScheduleSerializer(many = True, read_only = True)

    class Meta:
        model = Stud_Group
        fields = ['id', 'name', 'title', 'teacher', 'description', 
                  'number_of_lessons', 'rubric', 'students', 'lessons',
                  'schedule']


class RubricSerializer(serializers.ModelSerializer):
    stud_groups = Stud_GroupSerializer(many = True, read_only = True)
    
    class Meta:
        model = Rubric
        fields = ['id', 'name', 'image', 'stud_groups']
