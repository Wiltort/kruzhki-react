from rest_framework import serializers
from .models import (
    Rubric, Stud_Group, Lesson, Schedule_item,
    Schedule_template, Attending, Joining,
    )
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CurrentUserSerializer
from users.models import User
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction


class ScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_item
        fields = ('id', 'day_of_week', 'btime', 'template')


class ScheduleSerializer(serializers.ModelSerializer):
    items_set = ScheduleItemSerializer(many = True)
    
    class Meta:
        model = Schedule_template
        fields = ('id', 'group', 'items_set')
    
    def create(self, validated_data):



class AttendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attending
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)

    class Meta:
        model = Lesson
        fields = ('id', 'stud_group', 'ldate', 'topic', 'attending')


class StudentSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'stud_groups', 'attending', 'first_name', 'last_name')


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
    teacher = CurrentUserSerializer()
    rubric = RubricField(
        slug_field='id', queryset=Rubric.objects.all(), many=True
    )
    is_in_students = serializers.SerializerMethodField(method_name='get_is_in_students')
    is_teacher = serializers.SerializerMethodField(method_name='get_is_teacher')
    is_joining = serializers.SerializerMethodField(method_name='get_is_joining')
    image = Base64ImageField()

    class Meta:
        model = Stud_Group
        fields = ['id', 'name', 'title', 'teacher', 'description', 
                  'number_of_lessons', 'rubric', 'students', 'lessons',
                  'schedule', 'image', 'is_teacher', 'is_in_students', 'is_joining',
                  'begin_at']

    def get_is_in_students(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if request.user.is_staff:
            return False
        return request.user.stud_groups.filter(pk=obj.pk).exists()
    
    def get_is_teacher(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user == obj.teacher
    
    def get_is_joining(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Joining.objects.filter(user=request.user, group=obj).exists()


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
        fields = ('id', 'name', 'title', 'image', 'number_of_lessons')