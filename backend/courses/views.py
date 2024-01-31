from django.shortcuts import render
#from django.http import HttpResponse
from typing import Any
from django.db.models.query import QuerySet
from .models import Stud_Group, Rubric, Student
from rest_framework import viewsets
from .serializers import (
    Stud_GroupSerializer, 
    RubricSerializer, 
    StudentSerializer,
    )
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
    )
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrAllowedTeacher, IsAdminOrTeacher
    )
from rest_framework.pagination import PageNumberPagination
from django.views.generic import ListView


class RubricViewSet(viewsets.ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    #def perform_create(self, serializer):
    #    serializer.save(stud_groups = None)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Stud_Group.objects.all()
    serializer_class = Stud_GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAllowedTeacher]
    pagination_class = PageNumberPagination


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