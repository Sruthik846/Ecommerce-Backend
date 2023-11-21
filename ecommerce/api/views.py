import json
from django.http import JsonResponse
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
from django.shortcuts import render, get_object_or_404

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


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
        # print(request.data)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            # username = serializer.validated_data['username']
            # password = serializer.validated_data['password']

            username = request.data['username']
            password = request.data['password']

            print(username,password)
            # print(User.objects.get(password='12345'))
            user=authenticate(request,username=username,password=password)
            print('---------------------------------',user,'----------------------------------')
            if user is not None:
                login(request, user)
                print(f"logged successfully {user}")
                return Response({'login':True},status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@permission_classes([IsAuthenticated])
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        logout(request)
        print("Logged out successfully")
        return Response({'message':'Logged out successfully'})
    

@permission_classes([IsAuthenticated])
class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        categories = Category.objects.all().values('category', 'id') 
        return JsonResponse({'categories': list(categories)})

@permission_classes([IsAuthenticated])
class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)

        pname = request.data.get('pname')
        price = request.data.get('price')
        desc = request.data.get('description')
        status = request.data.get('status')
        quantity = request.data.get('quantity')
        category = request.data.get('category')
        images = request.data.getlist('files')

        category_id = Category.objects.get(id=category)
        print('------------ Category -----------------------',Category.objects.filter(id=category))
        print(pname,price,desc,status,quantity,category,images)
        # category_id = Category.objects.create(category= category)
        productData = Product(pname=pname,price=price,description=desc,status=status,quantity=quantity,category = category_id,image1= images[0],image2=images[1],image3=images[2],image4=images[3])
        productData.save()

        return Response({'success':'Product added'})

@permission_classes([IsAuthenticated])
class ProductListAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        productData = Product.objects.all()
        print(productData)
        productLatest = Product.objects.order_by('id')[:4]
        electronicProducts = Product.objects.filter(category=1)

        menProducts = Product.objects.filter(category=2)
        womenProducts = Product.objects.filter(category=3)
        babykidsProducts = Product.objects.filter(category=4)
        homeProducts = Product.objects.filter(category=5)
        sportsProducts = Product.objects.filter(category=6)
        bookProducts = Product.objects.filter(category=7)
        jwelleryProducts = Product.objects.filter(category=8)
        otherProducts = Product.objects.filter(category=9)
        if productData:
            serializer = ProductSerializer(productData, many=True)
            serializerLatest = ProductSerializer(productLatest, many=True)
            serializerElectronics = ProductSerializer(electronicProducts, many=True)
            serializerMen = ProductSerializer(menProducts, many=True)
            serializerWomen = ProductSerializer(womenProducts, many=True)
            serializerBabykids = ProductSerializer(babykidsProducts, many=True)
            serializerHome = ProductSerializer(homeProducts, many=True)
            serializerSports = ProductSerializer(sportsProducts, many=True)
            serializerBook = ProductSerializer(bookProducts, many=True)
            serializerjwellery = ProductSerializer(jwelleryProducts, many=True)
            serializerOthers = ProductSerializer(otherProducts, many=True)
            return Response({'All': serializer.data, 'Latest': serializerLatest.data,'Electronics':serializerElectronics.data,'men':serializerMen.data,'women':serializerWomen.data,
                            'babyKids':serializerBabykids.data,'home':serializerHome.data,'sports':serializerSports.data,'book':serializerBook.data,'jwellery':serializerjwellery.data,
                            'others':serializerOthers.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class DeleteProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self,request,id):
        Product.objects.get(id=id).delete()
        return Response(status=status.HTTP_200_OK)
    

@permission_classes([IsAuthenticated])
class ProductEditAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def put(self, request):
        try:
            obj = Product.objects.get(pk=request.data['id'])
        except Product.DoesNotExist:
            obj = None

        serializer = ProductSerializer(instance=obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("-------------- product edited -------------")
            return Response({'Success':'product Edited'},status=status.HTTP_200_OK)
        
        else:
            print('error',serializer.errors)
            return Response({'error':serializer.errors},status=500)

@permission_classes([IsAuthenticated])
class CartAPIView(APIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        cartdata = request.data
        organized_data = []

        # Loop through the dictionary
        index = 0  # Initialize the index
        item = {}  # Initialize an item dictionary
        for key, value in cartdata.items():
            # Extract the index and field from the key
            parts = key.split('[')
            current_index = int(parts[0])
            field = parts[1][:-1]  # Remove the trailing ']'

            # If the index changes, start a new item
            if current_index != index:
                if item:
                    organized_data.append(item)
                item = {}
                index = current_index

            item[field] = value

        # Add the last item to the organized_data
        if item:
            organized_data.append(item)

        # Now you have the data organized into a list of dictionaries
        for item in organized_data:
            username = item['user']
            if (UserDetails.objects.filter(name=username)):
                user_id = UserDetails.objects.get(name=username)
                if (Cart.objects.filter(name=item['name'])):
                    pdata = Cart.objects.get(name=item['name'])
                    pdata.selectedQuantity = item['selectedQuantity']
                    pdata.total = item['total']
                    pdata.save()
                else :
                    image = (item['url']).split('media/')[1]
                    Cart(name= item['name'], quantity= item['quantity'],price = item['price'],total = item['total'],image =image,selectedQuantity =item['selectedQuantity'],user=user_id).save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'cart added'},status=status.HTTP_200_OK)
    

    def get(self,request):
        # print(request.user)
        cartData = Cart.objects.all()
        if cartData:
            serializer = CartSerializer(cartData, many=True)
            product_data = [{
                'name': product.name,
                'quantity': product.quantity,
                'selectedQuantity': product.selectedQuantity,
                'price': product.price,
                'total': product.total,
                'image': product.image,
                'user': product.user.name  # Assuming 'name' is the field in the UserDetails model
            } for product in cartData]
            # print(product_data,serializer.data)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def delete(self,request,id):
        print(id)
        if Cart.objects.filter(name=id).exists():
            Cart.objects.get(name=id).delete()
            return Response({'success':'Product deleted successfully'},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

            





