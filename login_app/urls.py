from django.urls import path
from . import views

urlpatterns = [
    
    # login/
    path('', views.login_redirect, name="login_redirect"),

    # login/register
    path('register/', views.register, name="register"),

    # login/login
    path('login/', views.login, name="login")
]
