from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('store', views.store, name="store"),
    path('cart', views.cart, name="cart"),
    path('item/<int:id>', views.item, name="item"),
    path('checkout', views.checkout, name="checkout"),
    path('payment', views.payment, name="payment"),
    path('payment_page', views.payment_page, name="payment_page"),
    
    path('create_new_product', views.create_new_product, name="create_new_product"),
    path('all_products', views.all_products, name="all_products"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('edit/<int:product_id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('review/<int:product_id>', views.review, name="review"),
    path('delete_review/<int:product_id>/<int:review_id>', views.delete_review, name="delete_review"),
    path('delete_photo/<int:product_id>/<int:image_id>', views.delete_photo, name="delete_photo"),

    path('delete_cart_item/<int:cart_item_id>', views.delete_cart_item, name="delete_cart_item"),
]
