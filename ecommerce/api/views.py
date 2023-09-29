from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import *

from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login,logout


# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
   

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username='admin')
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })

class Signup(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        name = request.data['name']
        password = request.data['password']
        if serializer.is_valid():
            serializer.save()
            User.objects.create(username=name,password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'Plz contact Admin!'},status=500)
        


@permission_classes([IsAuthenticated])
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            # username = serializer.validated_data['username']
            # password = serializer.validated_data['password']

            username = request.data['username']
            password = request.data['password']

            print(username,password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(f"logged successfully {user}")
                return Response({'username':username,'password':password})
            
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)