from django.shortcuts import render
#from django.http import HttpResponse
from typing import Any
from django.db.models.query import QuerySet
from .models import Stud_Group, Rubric, Student
from rest_framework import viewsets, mixins
from .serializers import (
    Stud_GroupSerializer, 
    RubricSerializer, 
    StudentSerializer,
    AddStud_GroupSerializer
    )
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
    AllowAny
    )
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrAllowedTeacherOrReadOnly, IsAdminOrTeacher
    )
from rest_framework.pagination import PageNumberPagination
from django.views.generic import ListView
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RubricFilter


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

    

    



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]


class CoursesView(ListView):
    template_name = 'index.html'
    context_object_name = 'courses'
    model = Stud_Group
    

def index(request):
    courses = Stud_Group.objects.order_by('rubric')
    
    return render(request, "index.html", {"courses": courses})