from django.conf import settings
from django.db import models
from carts.models import Cart
from decimal import Decimal
from accounts.models import UserAddress

# Create your models here.


STATUS_CHOICES = (
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Finished', 'Finished')
)

try:
    tax_rate = settings.DEFAULT_TAX_RATE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='started')
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address',
                                         on_delete=models.CASCADE, default=1)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address',
                                        on_delete=models.CASCADE, default=1)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        instance.tax_total = Decimal(Decimal('%s' % tax_rate) * Decimal(self.sub_total)).quantize(two_places)
        instance.final_total = Decimal(self.sub_total) + Decimal(instance.tax_total)
        instance.save()
        return instance.final_total
