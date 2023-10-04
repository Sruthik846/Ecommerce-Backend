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
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

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
        email = request.data['email']
        if serializer.is_valid():
            serializer.save()
            User.objects.create_user(username=name,email=email,password=password)
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
            # print(User.objects.get(password='12345'))
            user=authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(f"logged successfully {user}")
                return Response({'username':username,'password':password},status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            print("product added")
            return Response({'Success':'product added'},status=status.HTTP_200_OK)
        
        else:
            print('error',serializer.errors)
            return Response({'error':serializer.errors},status=500)

@permission_classes([IsAuthenticated])
class ProductListAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        productData = Product.objects.all()
        productLatest = Product.objects.order_by('id')[:4]
        electronicProducts = Product.objects.filter(category='Electronics')
        if productData:
            serializer = ProductSerializer(productData, many=True)
            serializerLatest = ProductSerializer(productLatest, many=True)
            serializerElectronics = ProductSerializer(electronicProducts, many=True)
            return Response({'All': serializer.data, 'Latest': serializerLatest.data,'Electronics':serializerElectronics.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class DeleteProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self,request,id):
        Product.objects.get(id=id).delete()
        return Response(status=status.HTTP_200_OK)

        


