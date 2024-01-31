from django.urls import include, path
from .views import (
    RubricViewSet, GroupViewSet, StudentViewSet, index
    )
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('api/v1/rubrics', RubricViewSet)
router.register('api/v1/groups', GroupViewSet)
router.register('api/v1/students', StudentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index')
]