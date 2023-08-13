from calendar import c
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, requset):
        data = requset.data
        serializers = RegisterSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            user = User.objects.get(username=requset.data.get("username"))
            if user:
                refresh = RefreshToken.for_user(user=user)
                access = str(refresh.access_token)
                data = {"refresh_token": str(refresh), "access_token": access}
                return Response(data, status=status.HTTP_201_CREATED)
        return Response({"error": "please provied correct data"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')    
        password = request.data.get('password')
        try:
            user1 = User.objects.get(username=username)
        except Exception as E:
            return Response({"error1": "please provide username and password correctly"}, status=status.HTTP_400_BAD_REQUEST)
        print(user1.password)
        user = authenticate(**request.data)
        if user:
            refresh = RefreshToken.for_user(user=user1)
            access = str(refresh.access_token)
            data = {"refresh_token": str(refresh), "access_token": access}
            return Response(data, status=status.HTTP_201_CREATED)
            return Response({"sucess": "signed in sucessfully"}, status=status.HTTP_200_OK)
        return Response({"error": "please provide username and password correctly"}, status=status.HTTP_400_BAD_REQUEST)
        
