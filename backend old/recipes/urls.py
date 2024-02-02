from django.urls import include, path
from rest_framework.routers import DefaultRouter

from Groups.views import IngredientViewSet, GroupViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('Groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
