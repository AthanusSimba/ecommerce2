from django.contrib import admin
from django.urls import path
from .views import dismiss_marketing_message, email_signup

urlpatterns = [
    path('dismiss_marketing_message/', dismiss_marketing_message, name='dismiss_marketing_message'),
    path('email_signup/', email_signup, name='ajax_email_signup'),
]