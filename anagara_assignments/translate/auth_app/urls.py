from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="regiser"), 
    path("login/", LoginView.as_view(), name="login"), 
    path("jwttoken/", TokenObtainPairView.as_view(), name="jwttoken"), 
]
