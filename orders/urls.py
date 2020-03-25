from django.urls import path
from .views import checkout, orders
urlpatterns = [
    path('checkout/', checkout, name='checkout'),

    path('orders/', orders, name='user_orders'),
]
