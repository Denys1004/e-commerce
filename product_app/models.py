from django.db import models
from django.core.files.storage import FileSystemStorage
import uuid


#from login_app.models import User, Cart

class ProductManager(models.Manager):

    def create_product(self, postData, fileData):
        print('*'*30)
        print(postData)
        print('*'*30)
        
        new_product = self.create(name=postData['product_name'], price=postData['product_price'], description=postData['editor1'], stars = 0, count=0, average=0) 
        for picture in fileData.getlist('product_image'):
            Image.objects.create(name=picture.name, image=picture, product=new_product)

        if 'categories' in postData:
            for category_id in postData.getlist('categories'):
                new_product.categories.add(Category.objects.get(id=category_id)) 
        elif len(postData['new_category'])>0:
            category_list=postData['new_category'].split(', ')
            print(category_list)
            for category in category_list:
                currentCategories=Category.objects.filter(name=category)
                if len(currentCategories)>0:
                    category = Category.objects.get(id=currentCategories[0])
                    new_product.categories.add(category)  
                else:  
                    category=Category.objects.create(name=category)
                    new_product.categories.add(category)
        new_product.save()
        return new_product

        
    def update_product(self, postData, fileData, product_id):
        updated_product = Product.objects.get(id = product_id)
        updated_product.name = postData['product_name']
        updated_product.price = postData['product_price']
        updated_product.description = postData['editor1']
        updated_product.save()

        for picture in fileData.getlist('product_image'):
            Image.objects.create(name=picture.name, image=picture, product=updated_product)

        return updated_product
        


class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = models.FloatField()
    digital = models.BooleanField(default = False)
    description= models.TextField()
    stars = models.IntegerField(null = True)
    count = models.IntegerField(null = True)
    average = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProductManager()

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length = 100)
    products=models.ManyToManyField(Product, related_name='categories')
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    stars = models.IntegerField(null = True)
    review=models.TextField(null=True)
    poster=models.ForeignKey('login_app.User', related_name='reviews', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True)  							
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    user = models.ForeignKey('login_app.User', related_name='orders', on_delete=models.CASCADE, null = True)
    total_cost=models.FloatField(default=0.00)
    shipping_cost=models.FloatField(default=0.00)
    item_cost=models.FloatField(default=0.00)
    instructions=models.TextField(default='')
    complete = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

class BillingAddress(models.Model):
    user = models.ForeignKey('login_app.User', on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address

class Payment(models.Model):
    user=models.ForeignKey('login_app.User', related_name='cards', on_delete=models.CASCADE)
    order=models.OneToOneField(Order, on_delete=models.CASCADE)
    nickname=models.CharField(max_length=20)
    name=models.CharField(max_length=255)
    number=models.IntegerField()
    billing_address=models.OneToOneField(BillingAddress, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    exp=models.DateField()

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, related_name='order_items',on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    date_added = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    cart = models.ForeignKey('login_app.Cart', related_name='cart_items',on_delete=models.CASCADE)
    item_cost = models.FloatField(default=0.00)
    total_item_cost = models.FloatField(default=0.00)
    quantity = models.IntegerField(default = 1)
    date_added = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class ShippingAddress(models.Model):
    user = models.ForeignKey('login_app.User', on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length = 200)
    instructions= models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address

class Image(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='product_pictures')
    product=models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, default=None, blank=True, null = True)
    date_added = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)