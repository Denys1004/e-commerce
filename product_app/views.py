from django.shortcuts import render, redirect, HttpResponse
from product_app.models import *
from django.contrib.auth.decorators import login_required
from login_app.models import *
from django.core.paginator import Paginator
from django.urls import reverse

import stripe
stripe.api_key = "sk_test_51HKrLqAG7S0SBZ5Vzv38JaUu7fRpBfiSqc9vgXJQGBiVmisThWxM6HAfTH6BrLgTRzuvbBOPoo1E9hckGzb85Ax000ttUZYhkL"

# Create your views here.
def index(request):
    return redirect('/store')

def store(request):
    products = Product.objects.all()								
    paginator = Paginator(products, 6)									
    page = request.GET.get('page')													
    products = paginator.get_page(page)			
    context = {
        'products' : products,
        'first_three_categories':Category.objects.all()[:3],
        'additional_categories':Category.objects.all()[3:]
    }
    if 'user_id' in request.session:
        cur_user = User.objects.get(id = request.session["user_id"]) 
        num_items_in_cart = cur_user.cart.total_quantity
        context['num_items_in_cart']=num_items_in_cart
    
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
    cur_rating = product.average
    first_image = product.images.all()[1]
    additional_images = product.images.all().exclude(id=first_image.id)
    popular_products = Product.objects.filter(average = 5)
    if 'user_id' in request.session:
        cur_user = User.objects.get(id = request.session['user_id'])
        context = {
            'product':product,
            'first_image':first_image,
            'additional_images':additional_images,
            'num_items_in_cart':cur_user.cart.total_quantity,
            'all_reviews':product.reviews.all(),
            'cur_user':cur_user,
            'star_count':range(cur_rating),
            'popular_products': popular_products
        }
    if 'user_id' not in request.session:
        context = {
            'product':product,
            'first_image':first_image,
            'additional_images':additional_images,
            'all_reviews':product.reviews.all(),
            'star_count':range(cur_rating),
            'popular_products': popular_products
        }
    return render(request, 'item.html', context)



def create_new_product(request):
    if request.method == "GET":
        context={
            'catergories':Category.objects.all()
        }
        return render(request, 'create_product.html', context)
    else:
        print('*'*30)
        print(request.POST.getlist('categories'))
        print('*'*30)
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
        return HttpResponse(cart.total_quantity)




def edit(request, product_id):
    if request.method == "GET":
        context = {
            'needed_product': Product.objects.get(id = product_id)
        }
        return render(request, 'edit_product.html', context)
    else:
        updated_product = Product.objects.update_product(request.POST, request.FILES, product_id)
        return redirect(f'/edit/{product_id}')


# update quantity
def update_quantity(request, product_id):
    current_item = CartItem.objects.get(id=product_id)
    current_item_old_qty = current_item.quantity
    item_old_total_cost = current_item.total_item_cost

    current_item.quantity = int(request.POST['qty'])

    current_item.total_item_cost  = current_item.quantity * current_item.item_cost
    current_item.save()

    cur_user = User.objects.get(id = request.session['user_id'])
    cart = User.objects.get(id = request.session['user_id']).cart

    cart.total_quantity = (cart.total_quantity - current_item_old_qty) + current_item.quantity
    cart.save()
    cur_user.save()

    cur_user.cart.total_cost = (cur_user.cart.total_cost - item_old_total_cost) + current_item.total_item_cost
    cur_user.cart.save()
    if current_item.quantity == 0:
        current_item.delete()
    
    context = {
        'num_items_in_cart':cur_user.cart.total_quantity,
        'cur_user':cur_user,
        'product':current_item
    }

    return render(request, 'cart_partial.html', context)



def review(request, product_id):
    product = Product.objects.get(id = product_id)
    poster = User.objects.get(id = request.session['user_id'])
    if 'rating' in request.POST:
        product.stars = product.stars + int(request.POST['rating'])
        product.count = product.count + 1
        product.average = product.stars / product.count 
        product.save()
        Review.objects.create(review = request.POST['review'], poster=poster, product = product, stars = int(request.POST['rating']))
        return redirect(f'/item/{product.id}')
    else:
        Review.objects.create(review = request.POST['review'], poster=poster, product = product)
        return redirect(f'/item/{product.id}')


def search_product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    search_query = request.GET['query']

    if search_query != '' and search_query is not None:
        searched_query = products.filter(name__icontains = search_query) 
        # search by category
        searched_category = categories.filter(name__icontains = search_query)
        if 'user_id' in request.session:
            cur_user = User.objects.get(id = request.session['user_id'])
            context = {
                'num_items_in_cart':cur_user.cart.total_quantity,
                'searched_query': searched_query,
                'searched_category': searched_category
            }
        if 'user_id' not in request.session:
            context = {
                'searched_query': searched_query,
                'searched_category': searched_category
            }
    return render(request, 'search_result.html', context)



def delete_review(request, product_id, review_id):
    review = Review.objects.get(id = review_id)
    if review.stars:
        product = Product.objects.get(id = product_id)
        product.count = product.count - 1
        product.stars = product.stars - review.stars
        product.average = product.stars / product.count
        product.save()
    review.delete()
    return redirect(f'/item/{product_id}')


def delete_photo(request, product_id, image_id):
    product = Product.objects.get(id = product_id)
    image = Image.objects.get(id = image_id)
    image.delete()
    return redirect(f'/edit/{product_id}')


def delete_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id = cart_item_id)
    # print("*" * 30)
    cart = Cart.objects.get(id = request.session['cart_id'])
    cart.total_quantity = cart.total_quantity - cart_item.quantity
    cart.total_cost = cart.total_cost - (cart_item.item_cost*cart_item.quantity)
    cart.save()
    cart_item.delete()
    return redirect('/cart')




def payment(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        Shipping_address = ShippingAddress.objects.create(
            user = cur_user,
            address = request.POST['address'],
            city = request.POST['city'],
            state = request.POST['state'],
            zipcode = request.POST['zipcode'],
        )

    return redirect('/payment_page')

def payment_page(request):
    context = {
        'cur_user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'payment.html', context)


def delete(request, id):
    product = Product.objects.get(id = id)
    product.delete()
    return redirect('/all_products')



def qty_of_cart_items(request):
    cart = Cart.objects.get(id = request.session['cart_id'])
    items = cart.total_quantity
    return HttpResponse(f'{items}') 


def clear_cart(request):
    cart = Cart.objects.get(id = request.session['cart_id'])
    user=User.objects.get(id=request.session['user_id'])
    new_cart=Cart.objects.create()
    user.cart=new_cart
    user.save()
    cart.delete()
    request.session['cart_id'] = new_cart.id
    return redirect('/cart')

def profile(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    user_order = Order.objects.filter(user=cur_user)
    print('*' * 30)
    print(user_order)
    context = {
        'current_user': cur_user,
    }
    return render(request, 'profile.html', context)

def display_category(request, category_id):
    category=Category.objects.get(id=category_id)
    category_products=category.products.all()
    
    paginator = Paginator(category_products, 6)									
    page = request.GET.get('page')													
    category_products = paginator.get_page(page)			
    
    context = {
        'products':category_products,
    }

    return render(request, 'category_partial.html', context)

def charge(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    amount = float(cur_user.cart.total_cost)

    if request.method == 'POST':

        current_order =Order.objects.create(
            user = cur_user,
            total_cost = cur_user.cart.total_cost,
            complete = True
        )
        shipping_address = ShippingAddress.objects.filter(user=cur_user).last()
        print('shipping address ', shipping_address)
        print('8' * 40)
        print(current_order)
        print('8' * 40)
        shipping_address.order =  current_order
        shipping_address.save()
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['name'],
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount = int(amount * 100),
            currency='usd',
            description='online transations'
        )

    return redirect(reverse('success', args=[amount]))

def success(request, args):
    cur_user =  User.objects.get(id=request.session['user_id'])
    cart = cur_user.cart
    new_cart = Cart.objects.create()
    cur_user.cart = new_cart
    cur_user.save()
    cart.delete()
    amount = args
    context =  {
        'amount': amount,
        'cur_user': cur_user
    }
    return render(request, 'charges_success.html', context)
