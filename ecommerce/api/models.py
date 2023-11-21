from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=50 , null=True)
    email = models.CharField(max_length=50, null=True)
    mobileNo = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=500, null=True)

class Category(models.Model):
    category = models.CharField(max_length=100, null=True)


class Product(models.Model):
    pname = models.CharField(max_length=50 , null=True)
    price = models.CharField(max_length=50 , null=True)
    description = models.CharField(max_length=500 , null=True)
    status = models.CharField(max_length=50 , null=True)
    quantity = models.CharField(max_length=50 , null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='category_product')
    # imgUrl = models.ImageField(upload_to='products/', blank=True, null=True)
    image1 = models.ImageField(upload_to='images/',blank=True, null=True)
    image2 = models.ImageField(upload_to='images/',blank=True, null=True)
    image3 = models.ImageField(upload_to='images/',blank=True, null=True)
    image4 = models.ImageField(upload_to='images/',blank=True, null=True)


class Cart(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=50 , null=True)
    quantity = models.CharField(max_length=50 , null=True)
    selectedQuantity = models.CharField(max_length=50 , null=True)
    price = models.CharField(max_length=50 , null=True)
    total = models.CharField(max_length=500 , null=True)
    image = models.ImageField(upload_to='cart/',blank=True, null=True)


class Order(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    choices = (('Received', 'Received'),
        ('Scheduled', 'Scheduled'), 
        ('Shipped', 'Shipped'),
        ('In Progress','In Progress'),
        )
    order_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20,choices=choices)
    
    def __str__(self):
        return self.order_number
    
class OrderUpdates(models.Model):
    Order_id = models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    order_desc = models.CharField(max_length=100)
    
    
