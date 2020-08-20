from django.db import models
from django.contrib.auth.models import User
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

class ProductManager(models.Manager):
    def create_product(self, filedata):
        print('************************************************************')																	
        print(filedata)																	
        print('************************************************************')																	
        # new_product = self.create(
        #     name = postData['name']
        #     price = postData['price']
        #     if len(filedata) > 0:													
        #         # manage name of the file to prevent conflict
        #         for eachname in filedata:											
        #             file_name = filedata['product_image'].name   #saving filename .name is like .png								
        #             new_name = f"{file_name.split('.')[0]}-{uuid.uuid4().hex}.{file_name.split('.')[-1]}" # adding random string to the name		
        #             filedata['product_image'].name = new_name    # reassigning the existing name to new name	
        #             new_product.images.add(filedata['product_image'])
        #             new_product.save()		
        # )													
        return 'new_product'													



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = models.FloatField()
    images = ArrayField(models.ImageField(upload_to='product_images', default=None, blank=True, null = True))

    digital = models.BooleanField(default = False, null = True, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProductManager()

    def __str__(self):
        return self.name

# class Category
    # Many to many with Product

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    complete = models.BooleanField(default = False) # if complete is False that is open cart, and we can add items to it
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length = 200, null = False)
    city = models.CharField(max_length = 200, null = False)
    state = models.CharField(max_length = 200, null = False)
    zipcode = models.CharField(max_length = 200, null = False)
    date_added = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.address


