from django.shortcuts import render, get_object_or_404
from .models import (
    Stud_Group, 
    Rubric, 
    Joining, 
    Schedule_template,
    Ring
    )
from rest_framework import viewsets, mixins, status
from .serializers import (
    Stud_GroupSerializer, 
    RubricSerializer,
    AddStud_GroupSerializer,
    ShortGroupSerializer,
    ScheduleSerializer,
    RingSerializer
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
from .filters import RubricFilter, ScheduleFilter
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
    

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule_template.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (IsAdminOrTeacherOrReadOnly,)
    filterset_class = ScheduleFilter


class RingViewSet(viewsets.ModelViewSet):
    queryset = Ring.objects.all()
    serializer_class = RingSerializer
    permission_classes = (IsAdminOrReadOnly,)
    
    