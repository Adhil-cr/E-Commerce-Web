from django.shortcuts import render
from themes.models import SiteSettings
from products.models import Product

def Base(request):
    return render(request,'base.html') 

def home(request):
    banners = SiteSettings.objects.all()
    products = Product.objects.filter(delete_status=1) \
                              .order_by('-priority', '-created_date')[:12]

    return render(request, 'home.html', {
        'banners':banners,
        'products':products

    })

