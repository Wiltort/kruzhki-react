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
router.register('v1/messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'v1/groups/<int:pk>/schedule_items/', 
         GroupViewSet.as_view(actions={'get': 'get_schedule_items'})
    ),
    path(
        'v1/groups/<int:pk>/schedule_items/<int:item_pk>', 
         GroupViewSet.as_view(actions={'delete': 'delete_item'})
    ),
    path(
        'v1/groups/<int:pk>/schedule_items/',
        GroupViewSet.as_view(actions={'post': 'create_item'})
    ),
    path(
        'v1/groups/<int:pk>/schedule_items/<int:item_pk>', 
         GroupViewSet.as_view(actions={'post': 'update_item'})
    ),
    path(
        'v1/groups/<int:pk>/schedule_items/forming', 
         GroupViewSet.as_view(actions={'get': 'create_lessons'})
    ),
    
]