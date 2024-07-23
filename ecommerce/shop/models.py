from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    image=models.ImageField(upload_to='images',null=True,blank=True)
    p_name=models.TextField(max_length=20)
    desc=models.TextField(max_length=200)
    def __str__(self):
        return self.p_name

class Products(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.TextField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='images',null=True,blank=True)
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

