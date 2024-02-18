from rest_framework.routers import DefaultRouter
from django.urls import include, path


'''
router = DefaultRouter()
router.register('users', UserViewSet)
'''

urlpatterns = [
    #path('', include(router.urls)),
    path('v1/',include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    
]