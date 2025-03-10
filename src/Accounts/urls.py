from django.urls import path
from .views import RegisterView, LoginView, update_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-profile/', update_profile, name='update_profile'),
]
