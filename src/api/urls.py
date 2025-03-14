# api/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import ApiRootView, CustomTokenObtainPairView, api_user_info

# API router
router = DefaultRouter()
from accounts import views

urlpatterns = [
    # API root
    # path('', ApiRootView.as_view(), name='api-root'),
    
    # Authentication
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/user/', api_user_info, name='api_user_info'),
    path('auth/register/initiate/', views.initiate_registration, name='initiate_registration'),
    path('auth/register/complete/', views.complete_registration, name='complete_registration'),
]