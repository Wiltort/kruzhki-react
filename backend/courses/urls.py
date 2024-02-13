from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet, StudentViewSet
    )
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('v1/rubrics', RubricViewSet, basename='rubric')
router.register('v1/groups', GroupViewSet)
router.register('v1/students', StudentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]