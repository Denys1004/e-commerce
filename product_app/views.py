from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import *
# Create your views here.
# def index(request):
#     return render(request, 'main.html')

def store(request):
    context = {}
    return render(request, 'store.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)

def pay(request):
    context = {}
    return render(request, 'pay.html', context)

def create_new_product(request):
    if request.method == 'GET':
        return render(request, 'multipic.html')
    else:
        # fs=FileSystemStorage(location='media/product_pictures')
        # print('*'*30)
        # for picture in request.FILES.getlist('product_image'):
        #     pic=fs.save(picture.name, picture)
        #     url=fs.url(pic)
        # print('*'*30)
        Product.objects.create_product(request.POST, request.FILES)
        return redirect('/store')