# accounts/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserSessionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sessions', UserSessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]