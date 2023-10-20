
from django.urls import path
from . import views


urlpatterns = [
    path('signup/',views.Signup.as_view()),
    path('login/',views.LoginAPIView.as_view()),
    path('logout/',views.LogoutAPIView.as_view()),
    path('create/',views.ProductAPIView.as_view()),
    path('edit/',views.ProductEditAPIView.as_view()),
    path('productView/',views.ProductListAPIView.as_view()),
    path('delete/<int:id>/',views.DeleteProductAPIView.as_view()),
    path('cart/',views.CartAPIView.as_view()),
    path('cart/delete/<str:id>/',views.CartAPIView.as_view()),

    path('token/',views.CustomAuthToken.as_view()),
    path('api-token-auth/',views.ObtainAuthToken.as_view(),name='api-token-auth')
]

