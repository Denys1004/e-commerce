from django.db import models
import re													
import bcrypt
#from product_app.models import Cart
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode() # create the hash 
        cart = Cart.objects.create()
        return self.create(
            first_name=postData['first_name'], 
            last_name=postData['last_name'], 
            email=postData['email'], 
            password=pw_hash,
            cart = cart
        )
    # Checking login 
    def authenticate(self, email, password):
        user_with_email = self.filter(email = email)
        if not user_with_email: # we quering for all users with this email, and if its empty list:
            return False
        user = user_with_email[0] # if we do have user with that email in our system:
        return bcrypt.checkpw(password.encode(), user.password.encode()) # checkpw returns True of False

    def validator(self, postData):												
        errors = {}																										
        # NAME VALIDATION 	
        if len(postData['first_name']) < 2:											
            errors['first_name'] = 'First name should be atleast 2 characters long.'	
        if not postData['first_name'].isalpha() and postData['first_name'] != '':
            errors['first_name'] = 'First name must containt only letters.'
        if len(postData['last_name']) < 2:										
            errors['last_name'] = 'Last name should be atleast 2 characters long'
        if not postData['last_name'].isalpha() and postData['first_name'] != '':
            errors['last_name'] = 'Last name must containt only letters.'
        # EMAIL VALIDATION
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank."
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Email is not valid"
        result =  self.filter(email = postData['email'])
        if len(result) > 0:
            errors['email'] = "Email is already registered."
        # PASSWORD VALIDATION
        if len(postData['password']) < 3:
            errors['password'] = 'Password required, should be atleast 8 characters long.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Confirmation didn't match the password"
        return errors

class Cart(models.Model):
    total_cost=models.FloatField(default=0.00)
    total_quantity=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    first_name = models.CharField(max_length = 255)										
    last_name = models.CharField(max_length = 255)																			
    email = models.TextField()
    password = models.TextField()	
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True)							
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)									
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

