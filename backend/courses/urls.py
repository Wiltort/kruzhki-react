from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet, ScheduleViewSet, RingViewSet,
    JoiningViewSet, MessageViewSet, LessonViewSet, GroupListViewSet,
    AttendingOfGroupViewSet, AttendingViewSet
    )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('v1/rubrics', RubricViewSet, basename='rubric')
router.register('v1/groups', GroupViewSet)
router.register('v1/schedules', ScheduleViewSet)
router.register('v1/rings', RingViewSet)
router.register('v1/joinings', JoiningViewSet)
router.register('v1/messages', MessageViewSet, basename='messages')
router.register('v1/lessons', LessonViewSet)
router.register('v1/my-groups', GroupListViewSet, basename='group-list')
router.register('v1/my-attendings', AttendingOfGroupViewSet)
router.register('v1/attendings', AttendingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'v1/groups/<int:pk>/schedule_items/', 
         GroupViewSet.as_view(actions={'get': 'get_schedule_items',
                                       'post': 'create_item',
                                       'delete': 'delete_item'})
    ),
    path(
        'v1/groups/<int:pk>/schedule_items/<int:item_pk>', 
         GroupViewSet.as_view(actions={'patch': 'update_item'})
    ),
    path(
        'v1/groups/<int:pk>/forming', 
         GroupViewSet.as_view(actions={'post': 'create_lessons'})
    ),
]