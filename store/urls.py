from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('category/<int:category_id>/', views.category_products, name='category_products'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),

    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),

    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('orders/', views.orders, name='orders'),
]