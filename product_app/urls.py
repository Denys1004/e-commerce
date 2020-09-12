from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('store', views.store, name="store"),
    path('welcome', views.welcome, name="welcome"),
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

    path('<int:product_id>/update_quantity', views.update_quantity, name='update_quantity'),

    path('delete_cart_item/<int:cart_item_id>', views.delete_cart_item, name="delete_cart_item"),

    path('search_product', views.search_product, name='search_product'),
    path('display_category/<int:category_id>', views.display_category, name='display_category'),


    path('qty_of_cart_items', views.qty_of_cart_items, name="qty_of_cart_items"),
    path('clear_cart', views.clear_cart, name="clear_cart"),
    path('profile', views.profile, name='profile'),
    path('charge', views.charge, name='charge'),
    path('success/<str:args>',views.success, name='success' ),
    path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),
    path('remove_category/<int:category_id>/<int:product_id>', views.remove_category)
]
