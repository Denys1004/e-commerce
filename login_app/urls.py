from django.urls import path
from . import views

urlpatterns = [
    
    # login/
    path('', views.login_redirect, name="login_redirect"),

    # login/register
    path('register/', views.register, name="register"),

    # login/login
    path('login/<str:mess>', views.login, name="login"),

    # login/login
    path('logout/', views.logout, name="logout")
]
