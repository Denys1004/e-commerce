from django.contrib import admin

from .models import *
from login_app.models import *                  

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)

