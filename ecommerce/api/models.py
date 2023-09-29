from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=50 , null=True)
    email = models.CharField(max_length=50, null=True)
    mobileNo = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=500, null=True)