from django.contrib import admin
from .models import UserStripe, EmailConfirmed, UserAddress, UserDefaultAddress

# Register your models here.
admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'address', 'country', 'phone', 'shipping', 'billing']

    class Meta:
        model = UserAddress


admin.site.register(UserAddress, UserAddressAdmin)

admin.site.register(UserDefaultAddress)