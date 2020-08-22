from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('store', views.store, name="store"),
    path('cart', views.cart, name="cart"),
    path('item/<int:id>', views.item, name="item"),
    path('checkout', views.checkout, name="checkout"),
    path('create_new_product', views.create_new_product, name="create_new_product"),
    # path('update_product', views.update_product, name="update_product"),
    path('all_products', views.all_products, name="all_products"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart")
]
