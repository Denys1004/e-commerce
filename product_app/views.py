from django.shortcuts import render, redirect
from product_app.models import *

# Create your views here.
# def index(request):
#     return render(request, 'main.html')

def store(request):
    context = {
        'products':Product.objects.all()
    }
    return render(request, 'store.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)

def item(request, id):
    product=Product.objects.get(id=id)
    last=product.images.last()
    context = {
        'product':product,
        'additional_images':product.images.all().exclude(id=last.id)
    }
    return render(request, 'item.html', context)



def create_new_product(request):
    if request.method == "GET":
        return render(request, 'create_product.html')
    else:
        new_product = Product.objects.create_product(request.POST, request.FILES)
        return redirect('/store')