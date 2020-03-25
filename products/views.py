from django.shortcuts import render, Http404
from .models import Product, ProductImage
from marketing.models import MarketingMessage, Slider, MarketingManager


def home(request):
    sliders = Slider.objects.all_featured()
    print(sliders)
    products = Product.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    marketing_message = MarketingMessage.objects.get_featured_item().message

    try:

        request.session['marketing_message'] = MarketingMessage.objects.get_featured_item().message

    except:
        pass

    context = {
        'sliders': sliders,
        'products': products,
        'marketing_message': marketing_message
    }
    template = 'products/home.html'
    return render(request, template, context)


def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {
            'query': q,
            'products': products
        }
        template = 'products/results.html'
    else:
        template = 'products/home.html'
        context = {}
    return render(request, template, context)


def all(request):
    del request.session['marketing_message']
    products = Product.objects.all()
    template = 'products/all.html'
    context = {
        'products': products
    }
    return render(request, template, context)


def single(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        # images = product.productimage_set.all()
        images = ProductImage.objects.filter(product=product)
        template = 'products/single.html'
        context = {
            'product': product,
            'images': images
        }
        return render(request, template, context)
    except:
        raise Http404
