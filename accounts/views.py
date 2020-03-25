import re
from django.shortcuts import get_object_or_404
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserAddress, UserDefaultAddress
from django.contrib import messages


# Create your views here.

def logout_view(request):
    logout(request)
    messages.success(request, "Successifuly Logged out. Feel free to login again")
    return HttpResponseRedirect(reverse('home'))


def login_view(request):
    form = LoginForm(request.POST or None)
    btn = 'Login'
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, 'Successifuly Logged in. Welcome back.')
        user.emailconfirmed.activate_user_mail()
        return HttpResponseRedirect('/')
    context = {
        'form': form,
        'submit_btn': btn
    }
    return render(request, 'forms.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = 'Join'
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(request, 'Successifuly registered. Please confirm your mail now.')
        return HttpResponseRedirect('/')
    context = {
        'form': form,
        'submit_btn': btn
    }
    return render(request, 'forms.html', context)


SHA1_RE = re.compile(r'[a-f0-9_]')


def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        print('activation key is real')
        print(activation_key)
        try:
            instance = get_object_or_404(EmailConfirmed, activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, 'There was an error with your request')
            HttpResponseRedirect('/')

        if instance is not None and not instance.confirmed:
            page_message = 'Confirmation Successiful! Welcome.'
            instance.confirmed = True
            instance.save()
            messages.success(request, 'Successifuly Confirmed. Please Login.')

        elif instance is not None and instance.confirmed:
            page_message = 'Already Confirmed'
            messages.success(request, 'Already Confirmed.')

        else:
            page_message = ''
            pass
        context = {'page_message': page_message}

        return render(request, 'accounts/activation_complete.html', context)
    else:
        print('Your sha is not found')
        raise Http404


def add_user_address(request):
    print(request.GET)
    try:
        next_page = request.GET.get('next')
    except:
        redirect = None
    form = UserAddressForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data['default']
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()
            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page)))
    submit_btn = 'Save Address'
    form_title = 'Add New Address'
    return render(request, 'forms.html',
                  {'form': form,
                   'submit_btn': submit_btn,
                   'form_title': form_title}
                  )

