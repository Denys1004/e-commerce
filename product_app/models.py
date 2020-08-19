from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = models.FloatField()
    digital = models.BooleanField(default = False)
    images = ArrayField(models.ImageField(upload_to='product_images', default=None, null = True))
    description= models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)
    #image

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length = 100)
    products=models.ManytoManyField(Product, related_name='categories')
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    rating=models.FloatField(null=True)
    review=models.TextField(null=True)
    poster=models.ForeignKey(Customer, related_name=reviews, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, null = True)
    total_cost=models.FloatField(default=0.00)
    complete = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

class Payment(models.Model):
    customer=models.ForeignKey(Customer, related_name='cards', on_delete=models.CASCADE)
    order=models.OneToOneField(Order, related_name='card')
    name=models.CharField(max_length=255)
    number=models.IntegerField(max_length=16)
    exp=models.DateField()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, related_name='order_items',on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    date_added = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address

class BillingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address