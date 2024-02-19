from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet
    )
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('v1/rubrics', RubricViewSet, basename='rubric')
router.register('v1/groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    #path('v1/groups/my', )
]