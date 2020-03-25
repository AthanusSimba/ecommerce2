from django.urls import path
from .views import home, all, single, search

urlpatterns = [
    path('', home, name='home'),
    path('s/', search, name='search'),
    path('products/', all, name='products'),
    path('products/<slug>', single, name='single_product'),
]
