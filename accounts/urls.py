from django.urls import path
from .views import logout_view, login_view, registration_view, activation_view, add_user_address

urlpatterns = [
    path('logout/', logout_view, name='auth_logout'),
    path('login/', login_view, name='auth_login'),
    path('register/', registration_view, name='auth_register'),
    path('activate/<activation_key>', activation_view, name='activation_view'),
    path('add_user_address/', add_user_address, name='ajax_add_user_address'),
    path('add/', add_user_address, name='add_user_address')

]