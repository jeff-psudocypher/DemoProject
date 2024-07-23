from django.db import models
from shop.models import Products
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    data_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.quantity*self.product.price

class Order_table(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    phone=models.IntegerField()
    address=models.CharField(max_length=50)
    pin=models.IntegerField()
    ordered_date=models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(max_length=100,blank=True)
    payment_status=models.CharField(default='pending',max_length=30)
    delivery_status=models.CharField(default='pending',max_length=30)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    razorpay_payment_id=models.CharField(max_length=30)
    paid=models.BooleanField(default=False)

    def __str__(self):
        return self.name

