from django.urls import path
from .views import mycart, add_to_cart, remove_from_cart

urlpatterns = [
    path('cart/', mycart, name='cart'),
    path('cart/<slug>', add_to_cart, name='add_to_carts'),
    path('carts/<id>', remove_from_cart, name='remove_from_cart'),
]