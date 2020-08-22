from django.shortcuts import render, redirect
from product_app.models import *
from django.contrib.auth.decorators import login_required
from login_app.models import *

# Create your views here.
def index(request):
    return redirect('/login/login')

def store(request):
    if 'user_id' in request.session:
        cur_user = User.objects.get(id = request.session["user_id"]) 

        if len(cur_user.cart.cart_items.all()) > 0:
            num_items_in_cart = cur_user.cart.total_quantity
            context = {
                'products':Product.objects.all(),
                'num_items_in_cart':num_items_in_cart
            }
            return render(request, 'store.html', context)
        else:
            context = {
                'products':Product.objects.all()
            }
            return render(request, 'store.html', context)
    else:
        context = {
            'products':Product.objects.all()
        }
        return render(request, 'store.html', context)




def cart(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    cart_items = cur_user.cart.cart_items.all()
    for item in cart_items:
        print('PRICE: ', item.item_cost)
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user
    }
    return render(request, 'cart.html', context)





def checkout(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user
    }
    return render(request, 'checkout.html', context)






def item(request, id):
    product=Product.objects.get(id=id)
    last=product.images.last()
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'product':product,
        'additional_images':product.images.all().exclude(id=last.id),
        'num_items_in_cart':cur_user.cart.total_quantity
    }
    return render(request, 'item.html', context)


def create_new_product(request):
    if request.method == "GET":
        return render(request, 'create_product.html')
    else:
        new_product = Product.objects.create_product(request.POST, request.FILES)
        return redirect('/store')


def all_products(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        'all_products':Product.objects.all(),
        'num_items_in_cart':cur_user.cart.total_quantity
    }
    return render(request, 'all_products.html', context)


def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    cart = User.objects.get(id = request.session['user_id']).cart
    found_item = False

    all_cart_items = cart.cart_items.all()
    for item in all_cart_items:
        if item.product.id == product.id:
            found_item = True
            break
    
    if found_item:
        item.quantity += 1
        item.total_item_cost = item.product.price * item.quantity
        cart.total_cost += item.product.price
        cart.total_quantity+=1
        cart.save()
        item.save()
        return redirect('/store')
    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            item_cost = product.price,
            total_item_cost = product.price
        )
        cart.total_cost += product.price
        cart.total_quantity+=1
        cart.save()
        return redirect('/store')



def edit(request, id):
    if request.method == "GET":
        context = {
            'needed_product': Product.objects.get(id = id)
        }
        return render(request, 'edit_product.html', context)
    else:
        pass