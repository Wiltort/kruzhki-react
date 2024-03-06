from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet, ScheduleViewSet, RingViewSet,
    JoiningViewSet, MessageViewSet
    )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('v1/rubrics', RubricViewSet, basename='rubric')
router.register('v1/groups', GroupViewSet)
router.register('v1/schedules', ScheduleViewSet)
router.register('v1/rings', RingViewSet)
router.register('v1/joinings', JoiningViewSet)
router.register('v1/messages', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]