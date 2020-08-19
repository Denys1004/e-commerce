from django.urls import path
from reg_log import views


urlpatterns = [
  path('register', views.register, name='register')
]