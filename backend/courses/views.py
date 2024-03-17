from django.shortcuts import render, get_object_or_404
from .models import (
    Stud_Group, 
    Rubric, 
    Joining, 
    Schedule_template,
    Ring,
    Message,
    Schedule_item,
    Attending,
    Lesson
    )
from rest_framework import viewsets, mixins, status
from .serializers import (
    Stud_GroupSerializer, 
    RubricSerializer,
    AddStud_GroupSerializer,
    ShortGroupSerializer,
    ScheduleSerializer,
    RingSerializer,
    GetMessageSerializer,
    AddMessageSerializer,
    JoiningSerializer,
    ScheduleItemSerializer,
    AddScheduleItemSerializer,
    LessonSerializer,
    AttendingOfGroupSerializer,
    AttendingSerializer
    )
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
    AllowAny,
    )
from .permissions import (
    IsAdminOrAllowedTeacherOrReadOnly,
    IsAdminOrTeacher,
    IsAdminOrReadOnly,
    IsAdminOrTeacherOrReadOnly
    )
from django.views.generic import ListView
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RubricFilter, ScheduleFilter, JoiningFilter
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.response import Response



class RubricViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = (AllowAny,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Stud_Group.objects.all()
    permission_classes = (IsAdminOrAllowedTeacherOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RubricFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return Stud_GroupSerializer
        return AddStud_GroupSerializer
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(teacher=user)

    @action(
        detail=True,
        methods=('post','delete'),
        permission_classes=(IsAuthenticated,)
        )
    def join(self, request, pk=None):
        if request.method == 'POST':
            return self.add_group(Joining, request, pk)
        return self.delete_group(Joining, request, pk)
    
    def add_group(self, model, request, pk):
        group = get_object_or_404(Stud_Group, pk=pk)
        user = self.request.user
        if model.objects.filter(group=group, user=user).exists():
            raise ValidationError('Заявка уже отправлена')
        if user.stud_groups.filter(pk=group.pk).exists():
            raise ValidationError('Уже в группе')
        model.objects.create(group=group, user=user)
        serializer=ShortGroupSerializer(group)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_group(self, model, request, pk):
        group = get_object_or_404(Stud_Group, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, group=group, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def get_schedule_items(self, request, pk):
        group = Stud_Group.objects.get(id=pk)
        schedule, created = Schedule_template.objects.get_or_create(group=group)
        items = schedule.items.all()
        return Response(ScheduleItemSerializer(items, many=True).data)
    
    @action(
        methods=['DELETE'],
        detail=False,
        permission_classes=(IsAdminOrAllowedTeacherOrReadOnly,)
    )
    def delete_item(self, request, pk):
        group = Stud_Group.objects.get(id = pk)
        self.check_object_permissions(request=request,obj=group)
        template = Schedule_template.objects.get(group=group)
        items = template.items.all()
        for item in items:
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def create_item(self, request, pk):
        group = Stud_Group.objects.get(id = pk)
        self.check_object_permissions(request=request,obj=group)
        template, created = Schedule_template.objects.get_or_create(group=group)
        serializer = AddScheduleItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(template=template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        methods=['POST', 'PUT', 'PATCH'],
        detail=True,
        permission_classes=(IsAdminOrAllowedTeacherOrReadOnly,)
    )
    def update_item(self, request, pk, item_pk):
        group = Stud_Group.objects.get(id=pk)
        self.check_object_permissions(request=request,obj=group)
        item = get_object_or_404(Schedule_item, id = item_pk)
        if item.template.group != group:
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = (request.method in ['PUT','PATCH'])
        serializer = AddScheduleItemSerializer(item, data=request.data, partial=partial)
        template = Schedule_template.objects.get(group=group)
        if serializer.is_valid():
            serializer.save(template=template)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        methods=['POST'],
        detail=False,
        permission_classes=(IsAdminOrAllowedTeacherOrReadOnly,)
    )
    def create_lessons(self, request, pk):
        group = Stud_Group.objects.get(id=pk)
        self.check_object_permissions(request=request,obj=group)
        template = Schedule_template.objects.get(group=group)
        template.create_lessons()
        serializer = LessonSerializer(group.lessons, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule_template.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (IsAdminOrTeacherOrReadOnly, IsAuthenticated)
    filterset_class = ScheduleFilter

    def get_queryset(self):
        queryset = super(ScheduleViewSet, self).get_queryset()
        user = self.request.user
        if user.is_staff:
            queryset = queryset.filter(group__teacher=user)
        else:
            queryset = queryset.filter(group__students=user)
        return queryset
        

class LessonViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        queryset = super(LessonViewSet, self).get_queryset()
        user = self.request.user
        if user.is_staff:
            queryset = queryset.filter(stud_group__teacher=user)
        else:
            queryset = queryset.filter(stud_group__students=user)
        return queryset

class RingViewSet(viewsets.ModelViewSet):
    queryset = Ring.objects.all()
    serializer_class = RingSerializer
    permission_classes = (IsAdminOrReadOnly,)


class JoiningViewSet(viewsets.ModelViewSet):
    queryset = Joining.objects.all()
    permission_classes = (IsAdminOrTeacher,)
    filter_backends = (DjangoFilterBackend,)
    filterset_classes = JoiningFilter
    serializer_class = JoiningSerializer
    
    def get_queryset(self):
        queryset = super(JoiningViewSet, self).get_queryset()
        userId = self.request.user.id
        queryset = queryset.objects.filter(group__teacher__id=userId)
        return queryset
    
    @action(
        detail=True,
        methods=('delete',),
        permission_classes=(IsAdminOrTeacher)
        )
    def accept(self, request, pk=None):
        joining = get_object_or_404(Joining, pk=pk)
        student = joining.user
        group = joining.group
        if student in group.students.all():
            raise ValidationError('Уже в группе!')
        if request.user != group.teacher:
            raise ValidationError('Это не ваша группа!')
        Message.objects.create(
            sender = request.user,
            to = student,
            topic='Вы приняты!',
            text=f'Здравствуйте, {student.first_name}!\nПоздравляем, вы приняты'\
                f' в группу {group.name} - "{group.title}".\nС уважением, '\
                f'{request.user.first_name} {request.user.last_name}.'
        )
        group.students.add(student)
        joining.objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(
        detail=True,
        methods=('delete',),
        permission_classes=(IsAdminOrTeacher)
        )
    def reject(self, request, pk=None):
        joining = get_object_or_404(Joining, pk=pk)
        student = joining.user
        group = joining.group
        if student in group.students.all():
            raise ValidationError('Уже в группе!')
        if request.user != group.teacher:
            raise ValidationError('Это не ваша группа!')
        Message.objects.create(
            sender = request.user,
            to = student,
            topic='Вам отказано',
            text=f'Здравствуйте, {student.first_name}!\nК сожалению, мы не можем'\
                f' принять Вас в группу {group.name} - "{group.title}".\nС уважением, '\
                f'{request.user.first_name} {request.user.last_name}.'
        )
        joining.objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        queryset = Message.objects.filter(to=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetMessageSerializer
        return AddMessageSerializer
    
    def perform_create(self, serializer):
        sender = self.request.user
        serializer.save(sender=sender)


class AttendingOfGroupViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Stud_Group.objects.all()
    permission_classes = (IsAdminOrAllowedTeacherOrReadOnly,)
    serializer_class = AttendingOfGroupSerializer


class AttendingViewSet(viewsets.ModelViewSet):
    queryset = Attending.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AttendingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            pk = self.request.kwargs.get('pk')
        return super().get_queryset()