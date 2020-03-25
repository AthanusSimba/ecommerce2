from django.db import models
from django.core.mail import send_mail
from django.urls import reverse

import stripe
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.template.loader import render_to_string
import random
import hashlib
from django_countries.fields import CountryField

# Create your models here.
stripe.api_key = settings.STRIPE_SECRETE_KEY


class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey('UserAddress', on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='user_address_shipping_default')
    billing = models.ForeignKey('UserAddress', on_delete=models.CASCADE,
                                null=True, blank=True, related_name='user_address_billing_default')

    def __str__(self):
        return str(self.user.username)


class UserAddressManager(models.Manager):
    def get_billing_address(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = CountryField(multiple=False)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        return '%s, %s, %s, %s, %s' % (self.address, self.city, self.state, self.country, self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.stripe_id


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_mail(self):
        # activation_url = 'http://localhost:8000/activate/%s' % self.
        activation_url = '%s%s' % (settings.SITE_URL, reverse('activation_view', args=[self.activation_key]))
        context = {
            'activation_key': self.activation_key,
            'url': activation_url,
            'user': self.user.username
        }
        message = render_to_string('accounts/activation_message.txt', context)
        subject = 'Activate your Email'
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwags):
        send_mail(subject, message, from_email, [self.user.email], kwags)


stripe.api_key = settings.STRIPE_SECRETE_KEY


# def get_or_create_stripe(user):
#  # new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
#   try:
#       user.userstripe.stripe_id
#   except UserStripe.DoesNotExist:
#       customer = stripe.Customer.create(
#           email=user.email
#       )
#       new_user_stripe = UserStripe.objects.create(
#           user=user,
#           stripe_id=customer.id
#       )
#   except:
#       pass


# user_logged_in.connect(get_or_create_stripe)

def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email=user.email
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()


def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            base, domain = str(user.email).split('@')
            activation_key = hashlib.sha1((short_hash + base).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_mail()


post_save.connect(user_created, sender=settings.AUTH_USER_MODEL)
