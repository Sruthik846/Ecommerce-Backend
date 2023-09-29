
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.Signup.as_view()),
    path('login/',views.LoginAPIView.as_view()),
    path('token/',views.CustomAuthToken.as_view()),
]
