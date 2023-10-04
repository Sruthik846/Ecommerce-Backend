from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=50 , null=True)
    email = models.CharField(max_length=50, null=True)
    mobileNo = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=500, null=True)


class Product(models.Model):
    pname = models.CharField(max_length=50 , null=True)
    price = models.CharField(max_length=50 , null=True)
    description = models.CharField(max_length=500 , null=True)
    status = models.CharField(max_length=50 , null=True)
    quantity = models.CharField(max_length=50 , null=True)
    category = models.CharField(max_length=100, null=True)
    imgUrl = models.ImageField(upload_to='products/', blank=True, null=True)