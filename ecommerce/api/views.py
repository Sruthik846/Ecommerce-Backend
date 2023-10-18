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
        print(request.data)
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
                return Response({'login':True},status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@permission_classes([IsAuthenticated])
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        logout(request)
        return Response({'message':'Logged out successfully'})
    

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

        print(pname,price,desc,status,quantity,category,images)
        productData = Product(pname=pname,price=price,description=desc,status=status,quantity=quantity,category = category,image1= images[0],image2=images[1],image3=images[2],image4=images[3])
        productData.save()

        print('half saved')
        imagesdata = ProductImages(product=productData,image1= images[0],image2=images[1],image3=images[2],image4=images[3])
        # imagesdata =ProductImages.objects.create(product=productData,image1= images[0],image2=images[1],image3=images[2],image4=images[3])
        imagesdata.save()
        return Response({'success':'Product added'})
       
        # if serializer.is_valid():
        #     for image in images:
                
        #         print("product added")
        #         return Response({'Success':'product added'},status=status.HTTP_200_OK)
            
        # else:
        #     print('error',serializer.errors)
        #     return Response({'error':serializer.errors},status=500)


        # if serializer.is_valid():
        #     serializer.save()
        #     print("product added")
        #     return Response({'Success':'product added'},status=status.HTTP_200_OK)
        
        # else:
        #     print('error',serializer.errors)
        #     return Response({'error':serializer.errors},status=500)

@permission_classes([IsAuthenticated])
class ProductListAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        productData = Product.objects.all()
        productLatest = Product.objects.order_by('id')[:4]
        electronicProducts = Product.objects.filter(category='Electronics')
        menProducts = Product.objects.filter(category='Men')
        womenProducts = Product.objects.filter(category='Women')
        babykidsProducts = Product.objects.filter(category='Baby & Kids')
        homeProducts = Product.objects.filter(category='Home & furniture')
        sportsProducts = Product.objects.filter(category='Sports')
        bookProducts = Product.objects.filter(category='Books')
        jwelleryProducts = Product.objects.filter(category='Jwellery')
        otherProducts = Product.objects.filter(category='Others')
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
            print("-------------- product edited ")
            return Response({'Success':'product Edited'},status=status.HTTP_200_OK)
        
        else:
            print('error',serializer.errors)
            return Response({'error':serializer.errors},status=500)

@permission_classes([IsAuthenticated])
class CartAPIView(APIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print(request)
        return Response({'success':'cart added'})



