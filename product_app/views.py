from django.shortcuts import render, redirect

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