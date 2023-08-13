from django.urls import path
from .views import TranslationAPI

urlpatterns = [
    path('translate/', TranslationAPI.as_view(), name='translate'),
]
