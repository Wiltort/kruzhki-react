from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet, ScheduleViewSet
    )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('v1/rubrics', RubricViewSet, basename='rubric')
router.register('v1/groups', GroupViewSet)
router.register('v1/schedules', ScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]