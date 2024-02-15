from rest_framework import serializers
from .models import Rubric, Stud_Group, Student, Lesson, Schedule, Attending
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction


User = get_user_model()


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


class RubricSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rubric
        fields = ('__all__')


class RubricField(serializers.SlugRelatedField):
    
    def to_representation(self, value):
        request = self.context.get('request')
        context = {'request': request}
        serializer = RubricSerializer(value, context=context)
        return serializer.data


class Stud_GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many = True, read_only = True)
    lessons = LessonSerializer(many = True, read_only = True)
    schedule = ScheduleSerializer(many = True, read_only = True)
    teacher = UserSerializer()
    rubric = RubricField(
        slug_field='id', queryset=Rubric.objects.all(), many=True
    )
    is_in_students = serializers.SerializerMethodField(method_name='get_is_in_students')
    is_teacher = serializers.SerializerMethodField(method_name='get_is_teacher')
    image = Base64ImageField()

    class Meta:
        model = Stud_Group
        fields = ['id', 'name', 'title', 'teacher', 'description', 
                  'number_of_lessons', 'rubric', 'students', 'lessons',
                  'schedule', 'image', 'is_teacher', 'is_in_students']

    def get_is_in_students(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Student.objects.filter(user=request.user, in_group=obj).exists()
    
    def get_is_teacher(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user == obj.teacher


class AddStud_GroupSerializer(serializers.ModelSerializer):
    rubric = serializers.PrimaryKeyRelatedField(
        queryset=Rubric.objects.all(),
    )
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Stud_Group
        fields = (
            'rubric',
            'name',
            'title',
            'image',
            'description',
            'number_of_lessons'
        )
    
    def to_representation(self, instance):
        serializer = Stud_GroupSerializer(instance)
        return serializer.data
    
    @transaction.atomic
    def create(self, validated_data):
        rubric = validated_data.pop('rubric')
        st_group = Stud_Group.objects.create(**validated_data)
        st_group.rubric.set(rubric)
        st_group.save()
        #self.create... создать расписание и уроки
        return st_group
    
    @transaction.atomic
    def update(self, instance, validated_data):
        rubric = validated_data.pop('rubric')
        instance.rubric.clear()
        instance.rubric.set(rubric)
        return super().update(instance, validated_data)
    
    def validate(self, data):
        rub = data['rubric']
        if not rub:
            raise serializers.ValidationError(
                'Поле "Рубрика" не может быть пустым'
            )
        if data['number_of_lessons']<=0:
            raise serializers.ValidationError(
                'Количество уроков не может быть меньше 1'
            )
        return data
    

class ShortGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stud_Group
        fields = ('id', 'name', 'title', 'image')