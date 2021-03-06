from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def login_redirect(request):
    return redirect(f'/login/login/{log}')

# REGISTRATION
def register(request):
    if request.method == "GET":
        return render(request, "login_app/register.html")
    else:
        request.session.clear()
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        errors = User.objects.validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/login/register/')
        new_user = User.objects.register(request.POST)
        request.session.clear()
        request.session['user_id'] = new_user.id
        request.session['cart_id'] = new_user.cart.id

        return redirect('/welcome')

# LOGIN
def login(request, mess):
    if request.method == "GET":
        if 'first_name' in request.session:
            request.session.clear()
            return render(request, "login_app/login.html")
        else:
            if mess == 'mess':
                print('*' * 30)
                print(mess)
                print('*' * 30)
                messages.success(request, "In order to buy products you need to login")
            return render(request, "login_app/login.html")
    else:
        result = User.objects.authenticate(request.POST['email'],request.POST['password']) # Checking login
        if result == False:
            messages.error(request, "Email or passwort do not match.")
            return redirect('/login/login/reg')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            request.session['cart_id'] = user.cart.id
            return redirect('/welcome')
        
def logout(request):
    request.session.clear()
    return redirect('/welcome')