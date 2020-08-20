from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('create_new_product', views.create_new_product),
    path('pay/', views.pay, name='pay')
]
