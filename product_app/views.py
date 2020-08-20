from django.shortcuts import render, redirect
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

def item(request):
    context = {}
    return render(request, 'item.html', context)

def create_new_product(request):
    Product.objects.create_product(request.FILES)
    return redirect('/store')