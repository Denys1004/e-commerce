from django.urls import path
from reg_log import views


urlpatterns = [
  path('register', views.register, name='register'),
  path('user_login', views.user_login, name='user_login'),
  path('user_logout', views.user_logout, name='user_logout'),
]