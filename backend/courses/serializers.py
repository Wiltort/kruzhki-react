from rest_framework import serializers
from .models import (
    Rubric, Stud_Group, Lesson, Schedule_item,
    Schedule_template, Attending, Joining, Days, Ring, Message)
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CurrentUserSerializer
from users.models import User
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction


class RingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ring
        fields = '__all__'


class ScheduleItemSerializer(serializers.ModelSerializer):
    day_of_week = serializers.SerializerMethodField(method_name='weekday')
    btime = serializers.ReadOnlyField(source = 'btime.begin_at')
    etime = serializers.ReadOnlyField(source = 'btime.end_at')
    class Meta:
        model = Schedule_item
        fields = ('id', 'day_of_week', 'btime', 'etime', 'template')
    def weekday(self, obj):
        return Days(obj.day_of_week).label
    

class AddScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_item
        fields = ('day_of_week', 'btime', 'template')

class ScheduleSerializer(serializers.ModelSerializer):
    items = ScheduleItemSerializer(many = True)
    
    class Meta:
        model = Schedule_template
        fields = ('id', 'group', 'items')
    
    @transaction.atomic
    def create(self, validated_data):
        if 'items' not in validated_data:
            template = Schedule_template.create(**validated_data)
            return template
        items_set = validated_data.pop('items')
        template = Schedule_template.objects.create(**validated_data)
        for item in items_set:
            Schedule_item.objects.get_or_create(**item, template=template)
        template.create_lessons()
        return template

    @transaction.atomic    
    def update(self, instance, validated_data):
        instance.group = validated_data.get('group', instance.group)
        instance.save()
        if 'items' not in validated_data:
            instance.delete_lessons()
            return instance
        items_set = validated_data.pop('items')
        for item in items_set:
            Schedule_item.objects.get_or_create(**item, template=instance)
        instance.create_lessons()
        return instance
    

class AttendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attending
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)

    class Meta:
        model = Lesson
        fields = ('id', 'ldate', 'topic', 'attending')


class StudentSerializer(serializers.ModelSerializer):
    attending = AttendingSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


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
    schedule_templates = ScheduleSerializer(many = True, read_only = True)
    teacher = CurrentUserSerializer()
    rubric = RubricField(
        slug_field='id', queryset=Rubric.objects.all(), many=True
    )
    is_in_students = serializers.SerializerMethodField(method_name='get_is_in_students')
    is_teacher = serializers.SerializerMethodField(method_name='get_is_teacher')
    is_joining = serializers.SerializerMethodField(method_name='get_is_joining')
    image = Base64ImageField()
    is_staff = serializers.SerializerMethodField(method_name='get_is_staff')
    class Meta:
        model = Stud_Group
        fields = ['id', 'name', 'title', 'teacher', 'description', 
                  'number_of_lessons', 'rubric', 'students',
                  'schedule_templates', 'image', 'is_teacher', 'is_in_students', 'is_joining',
                  'begin_at', 'is_staff']

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

    def get_is_staff(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if request.user.is_staff:
            return True


class AddStud_GroupSerializer(serializers.ModelSerializer):
    rubric = serializers.PrimaryKeyRelatedField(
        queryset=Rubric.objects.all(),
        many = True
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
            'number_of_lessons',
            'begin_at'
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
        Schedule_template.objects.create(group=st_group)
        #self.create... создать расписание и уроки
        return st_group
    
    @transaction.atomic
    def update(self, instance, validated_data):
        rubric = validated_data.pop('rubric')
        instance.rubric.clear()
        instance.rubric.set(rubric)
        if not Schedule_template.objects.filter(group=instance).exists():
            Schedule_template.objects.create(group=instance)
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


class AddMessageSerializer(serializers.ModelSerializer):
    to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    class Meta:
        model = Message
        fields = ('sender', 'to', 'topic', 'text')
    
class GetMessageSerializer(serializers.ModelSerializer):
    sender = CurrentUserSerializer()
    
    class Meta:
        model = Message
        fields = ('sender', 'topic', 'text', 'date')


class JoiningSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=False)
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Stud_Group.objects.all()
    )
    
    class Meta:
        model = Joining
        fields = ('user', 'group', 'date')


class AttendingOfGroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many = True, read_only = True)
    lessons = LessonSerializer(many = True, read_only = True)
    class Meta:
        model = Stud_Group
        fields = ['id', 'name', 'title', 'teacher', 'students', 'image', 'begin_at']
