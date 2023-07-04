from django.db import models
from Accounts.models import *
from Products.models import *

# Create your models here.
# class Cart(models.Model):
#     creation_date = models.DateTimeField(auto_now_add=True)

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ForeignKey(Products, on_delete=models.CASCADE)

#     quantity = models.PositiveIntegerField(default=1)
#     total = models.FloatField(default=0.00)

#     def __str__(self):
#         return f"{self.products.Product_Name} X {self.quantity}"
    
#     @property
#     def total_price(self):
#         total = self.quantity * self.products.Special_Price
#         total_amount = format(total, '0.2f')
#         return total_amount
#     # total_price = property(total_price)