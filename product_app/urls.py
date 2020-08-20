from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart', views.cart, name="cart"),
    path('item', views.item, name="item"),
    path('checkout', views.checkout, name="checkout"),
    path('create_new_product', views.create_new_product, name="create_new_product"),
]
