from http import client
import unittest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TranslationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", password="test_password") 
        self.token = self.get_access_token()
    
    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        return access_token

    def testt_translation_api(self):
        url = reverse("translate")
        query_params = "?source=EN&target=hi&text=hi+hello"
        response = self.client.get(url+query_params, HTTP_AUTHORIZATION= f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('source_text', response.data)
        self.assertIn('translated_text', response.data)
        self.assertIn('source_language', response.data)
        self.assertIn('target_language', response.data)   

    def test_invalid_request(self):
        url = reverse('translate')
        query_params = "?source=EN&target=hi"
        response = self.client.get(url+query_params,  HTTP_AUTHORIZATION= f'Bearer {self.token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data) 

if __name__ == "__main__":
    unittest.main()