from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth import get_user_model
from .models import UserAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
User = get_user_model()


class UserAddressForm(ModelForm):
    '''address = forms.CharField(required=True)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=True)
    state = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield(
        required=True)
    zipcode = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    shipping = forms.BooleanField()
    billing = forms.BooleanField()'''
    default = forms.BooleanField(label='Make Default')

    class Meta:
        model = UserAddress
        fields = ['address', 'address2', 'city', 'state', 'country', 'zipcode', 'phone']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Username not found')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError('Invalid Password ')
        elif user is None:
            pass
        else:
            return password


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Your Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError('This email seems registered')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
